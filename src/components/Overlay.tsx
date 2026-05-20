import React, { useMemo } from 'react';
import DOMPurify from 'dompurify';

interface OverlayProps {
  /** Content to render. Can be a string of HTML or JSX. */
  children: React.ReactNode | string;
  /** If true, touch events pass through to elements behind the overlay. If false (default), the overlay blocks interactions. */
  allowTouch?: boolean;
  /** Optional className for styling. */
  className?: string;
  /** Optional inline styles. */
  style?: React.CSSProperties;
}

/**
 * Overlay component that sanitizes string content and controls touch event behavior.
 * 
 * - By default (allowTouch=false), it acts as a barrier, blocking interactions with underlying elements.
 * - When allowTouch=true, it becomes click-through, allowing interactions with elements behind it.
 */
const Overlay: React.FC<OverlayProps> = ({
  children,
  allowTouch = false,
  className = '',
  style = {},
}) => {
  // Memoize sanitization to avoid performance hits on re-renders
  const sanitizedContent = useMemo(() => {
    if (typeof children !== 'string') return null;

    try {
      return DOMPurify.sanitize(children, {
        ALLOWED_TAGS: ['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'b', 'i', 'strong', 'em', 'br', 'img', 'ul', 'ol', 'li'],
        ALLOWED_ATTR: ['href', 'src', 'alt', 'class', 'style', 'target', 'rel'],
      });
    } catch (error) {
      console.error('Content sanitization failed:', error);
      return null;
    }
  }, [children]);

  // Logic: 
  // allowTouch = false (Default) -> pointer-events: auto (Blocks background)
  // allowTouch = true -> pointer-events: none (Allows background interaction)
  const pointerEvents = allowTouch ? 'none' : 'auto';

  return (
    <div
      className={`overlay ${className}`}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0,0,0,0.5)',
        pointerEvents, // Corrected logic: 'auto' blocks, 'none' allows
        ...style,
      }}
      data-testid="overlay-container"
    >
      {typeof children === 'string' ? (
        <div
          dangerouslySetInnerHTML={{ __html: sanitizedContent! }}
          data-testid="overlay-sanitized"
        />
      ) : (
        children
      )}
    </div>
  );
};

export default Overlay;