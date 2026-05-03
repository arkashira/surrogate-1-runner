
const TOKEN_CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // Crockford's base32 without 0,1,I,O
const TOKEN_LENGTH = 6;

function slugify(text: string): string {
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '-')           // spaces to -
    .replace(/[^\w\-]+/g, '')       // remove non-word chars
    .replace(/\-\-+/g, '-')         // collapse multiple -
    .replace(/^-+/, '')             // trim - from start
    .replace(/-+$/, '');            // trim - from end
}

function generateShortToken(): string {
  const bytes = new Uint8Array(TOKEN_LENGTH);
  crypto.getRandomValues(bytes);
  let token = '';
  for (let i = 0; i < TOKEN_LENGTH; i++) {
    token += TOKEN_CHARS[bytes[i] % TOKEN_CHARS.length];
  }
  return token;
}

export function generatePublicUrl(
  title: string,
  type: string,
  owner: string,
  slaTarget?: string | null
): string {
  const slug = slugify(title);
  const typeSlug = slugify(type);
  const ownerSlug = slugify(owner);
  const token = generateShortToken();

  // Include SLA fragment only if provided and valid-ish (keeps URL deterministic-ish)
  const suffix = slaTarget ? `-${slugify(slaTarget)}` : '';
  return `/${slug}-${typeSlug}-${ownerSlug}${suffix}-${token}`;
}