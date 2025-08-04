class HTMLSanitizer {
    constructor() {
        
        this.trustedDomains = [
            'localhost',
            'epa.gov'
        ];
        
        this.maxElements = 500;
        this.maxBase64Size = 10 * 1024 * 1024; // 10MB
        
        this.allowedElements = {
            'div': ['class', 'id', 'style'],
            'span': ['class', 'id', 'style'],
            'p': ['class', 'id', 'style'],
            'table': ['class', 'id', 'style'],
            'thead': ['class', 'id', 'style'],
            'tbody': ['class', 'id', 'style'],
            'tr': ['class', 'id', 'style'],
            'td': ['class', 'id', 'style', 'colspan', 'rowspan'],
            'th': ['class', 'id', 'style', 'colspan', 'rowspan'],
            'img': ['src', 'alt', 'width', 'height', 'class', 'id'],
            'h1': ['class', 'id', 'style'],
            'h2': ['class', 'id', 'style'],
            'h3': ['class', 'id', 'style'],
            'h4': ['class', 'id', 'style'],
            'h5': ['class', 'id', 'style'],
            'h6': ['class', 'id', 'style'],
            'br': [],
            'strong': ['class', 'id'],
            'b': ['class', 'id'],
            'em': ['class', 'id'],
            'sup': ['class', 'id'],
            'sub': ['class', 'id'],
            'svg': ['width', 'height', 'viewBox', 'class', 'id'],
            'g': ['transform', 'fill', 'stroke', 'class', 'id'],
            'path': ['d', 'stroke', 'fill', 'class', 'id'],
            'text': ['x', 'y', 'class', 'id']
        };
        
        this.allowedCSSProps = [
            'color', 'background-color', 'font-size', 'font-family', 'font-weight',
            'text-align', 'margin', 'padding', 'border', 'width', 'height',
            'display', 'opacity'
        ];
    }
    
    sanitizeElements(elements) {
        if (!Array.isArray(elements)) {
            throw new Error('Elements must be an array');
        }
        
        if (elements.length > this.maxElements) {
            throw new Error(`Too many elements. Max: ${this.maxElements}`);
        }
        
        return elements.map((el, i) => {
            try {
                return this.sanitizeElement(el);
            } catch (error) {
                console.warn(`Error sanitizing element ${i}:`, error);
                return null;
            }
        }).filter(Boolean);
    }
    
    sanitizeElement(element) {
        if (!element || element.nodeType !== Node.ELEMENT_NODE) {
            return null;
        }
        const clone = element.cloneNode(true);
        this.removeDangerousElements(clone);
        this.sanitizeAttributes(clone);
        return clone.outerHTML;
    }

    removeDangerousElements(element) {
        const dangerous = element.querySelectorAll('script, object, embed, iframe');
        dangerous.forEach(el => el.remove());
        
        const allElements = [element, ...element.querySelectorAll('*')];
        allElements.forEach(el => {
            [...el.attributes].forEach(attr => {
                if (attr.name.toLowerCase().startsWith('on')) {
                    el.removeAttribute(attr.name);
                }
            });
        });
    }
    
    sanitizeAttributes(rootElement) {
        const allElements = [rootElement, ...rootElement.querySelectorAll('*')];
        
        allElements.forEach(element => {
            const tagName = element.tagName?.toLowerCase();
            const allowedAttrs = this.allowedElements[tagName] || ['class', 'id'];
            
            [...element.attributes].forEach(attr => {
                const attrName = attr.name.toLowerCase();
                
                if (!allowedAttrs.includes(attrName)) {
                    element.removeAttribute(attr.name);
                } else {
                    const sanitizedValue = this.sanitizeAttributeValue(attrName, attr.value);
                    element.setAttribute(attr.name, sanitizedValue);
                }
            });
        });
    }

    sanitizeAttributeValue(attrName, value) {
        if (!value) return '';
        
        const dangerousProtocols = ['javascript:', 'vbscript:', 'data:text/html'];
        if (dangerousProtocols.some(protocol => value.toLowerCase().includes(protocol))) {
            return '';
        }
        
        switch (attrName) {
            case 'src':
                return this.sanitizeSrc(value);
            case 'style':
                return this.sanitizeStyle(value);
            case 'class':
                return value.replace(/[^a-zA-Z0-9\-_\s]/g, '').trim();
            case 'id':
                return value.replace(/[^a-zA-Z0-9\-_]/g, '');
            default:
                return value.replace(/[<>"'&\n\r\t]/g, '').trim();
        }
    }

    sanitizeSrc(value) {
        if (value.startsWith('data:image/')) {
            return this.isValidBase64Image(value) ? value : '';
        }
        
        if (value.startsWith('/')) {
            return value;
        }
        
        if (value.startsWith('http')) {

            console.log("Starts with http: ", value);

            // try {
            //     const url = new URL(value);
            //     return this.trustedDomains.includes(url.hostname) ? value : '';
            // } catch {
            //     return '';
            // }
        }
        
        return '';
    }
    
    isValidBase64Image(dataUrl) {
        const pattern = /^data:image\/(png|jpeg|jpg|gif|webp);base64,([A-Za-z0-9+/=]+)$/i;
        const match = dataUrl.match(pattern);
        
        if (!match || dataUrl.length > this.maxBase64Size) {
            return false;
        }
        
        try {
            atob(match[2]);
            return true;
        } catch {
            return false;
        }
    }

    sanitizeStyle(value) {
        // Remove dangerous CSS patterns
        const dangerous = [
            /expression\s*\(/gi,
            /javascript:/gi,
            /vbscript:/gi,
            /url\s*\(\s*(?!data:image)/gi,
            /@import/gi,
            /behavior/gi
        ];
        
        let sanitized = value;
        dangerous.forEach(pattern => {
            sanitized = sanitized.replace(pattern, '');
        });
        
        // Filter to allowed CSS properties only
        const rules = sanitized.split(';').filter(rule => rule.trim());
        const validRules = rules.filter(rule => {
            const property = rule.split(':')[0]?.trim().toLowerCase();
            return this.allowedCSSProps.includes(property);
        });
        
        return validRules.join('; ');
    }
}

// Simplified main function
function sanitizeForPDF(elements) {

    console.log("sanitizeForPDF called!!");

    try {
        const sanitizer = new HTMLSanitizer();
        const elementsArray = Array.isArray(elements) ? elements : 
                             elements.toArray ? elements.toArray() : [elements];
        return sanitizer.sanitizeElements(elementsArray);
    } catch (error) {
        console.error('Sanitization failed:', error);
        throw error;
    }
}