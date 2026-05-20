import React, { useCallback, useMemo } from 'react';
import DOMPurify from 'dompurify';

export interface OverlayProps {
  /** Content to render inside the overlay.  Either a string (HTML) or a React node. */
  content?: string | React.ReactNode;
  /** Block touch events unless explicitly allowed.  Default: `false`. */
  allowTouchEvents?: boolean;
  /** Additional CSS class name(s). */
  className?: string;
  /** Whether the overlay is rendered.  Default: `true`. */
  isVisible?: boolean;
  /** Callback when the overlay is clicked. */
  onClick?: () => void;
  /** z‑index for stacking order.  Default: `1000`. */
  zIndex?: number;
}

/**
 * Sanitizes a string of HTML using DOMPurify.
 * The configuration is intentionally permissive for common markup but blocks
 * dangerous tags/attributes.
 */
const sanitizeContent = (content: string): string => {
  if (!content) return '';

  const config: DOMPurify.Config = {
    ALLOWED_TAGS: [
      'h1','h2','h3','h4','h5','h6',
      'p','br','hr',
      'ul','ol','li',
      'a','span','div','section','article',
      'strong','em','b','i','u','s',
      'img','figure','figcaption',
      'table','thead','tbody','tr','th','td',
      'button','input','label',
      'svg','path','circle','rect',
    ],
    ALLOWED_ATTR: [
      'href','src','alt','title','class','className',
      'id','style','type','value','placeholder',
      'width','height','viewBox','fill','stroke',
      'data-testid','aria-label','role',
    ],
    ALLOW_DATA_ATTR: false,
    FORBID_TAGS: ['script','iframe','object','embed','form','input','link'],
    FORBID_ATTR: ['onerror','onload','onclick','onmouseover','onfocus'],
  };

  return DOMPurify.sanitize(content, config);
};

export const Overlay: React.FC<OverlayProps> = ({
  content,
  allowTouchEvents = false,
  className = '',
  isVisible = true,
  onClick,
  zIndex = 1000,
}) => {
  /* ---------- 1️⃣  Sanitize string content ---------- */
  const sanitizedContent = useMemo(() => {
    return typeof content === 'string' ? sanitizeContent(content) : content;
  }, [content]);

  /* ---------- 2️⃣  Touch‑event handlers ---------- */
  const blockTouch = useCallback(
    (e: React.TouchEvent) => {
      if (!allowTouchEvents) {
        e.preventDefault();
        e.stopPropagation();
      }
    },
    [allowTouchEvents]
  );

  const handleClick = useCallback(
    (e: React.MouseEvent) => {
      if (!allowTouchEvents) {
        e.preventDefault();
        e.stopPropagation();
      }
      onClick?.();
    },
    [allowTouchEvents, onClick]
  );

  /* ---------- 3️⃣  Styles ---------- */
  const overlayStyles: React.CSSProperties = {
    position: 'fixed',
    inset: 0,
    zIndex,
    ...(allowTouchEvents
      ? {}
      : { touchAction: 'none', pointerEvents: 'auto' }),
  };

  /* ---------- 4️⃣  Render ---------- */
  if (!isVisible) return null;

  return (
    <div
      className={`overlay ${className}`.trim()}
      style={overlayStyles}
      onClick={handleClick}
      onTouchStart={blockTouch}
      onTouchMove={blockTouch}
      onTouchEnd={blockTouch}
      role="presentation"
      aria-hidden="true"
    >
      {typeof sanitizedContent === 'string' ? (
        <div
          /* eslint-disable-next-line react/no-danger */
          dangerouslySetInnerHTML={{ __html: sanitizedContent }}
        />
      ) : (
        sanitizedContent
      )}
    </div>
  );
};

export default Overlay;