export type Document = {
  id: string;
  title: string;
  authors: string[];
  year: number;
  url: string; // PDF or external link
  isPDF: boolean;
  summary?: string;
  thumbnail?: string; // data URL or remote small image
};

// Mock data — in production this comes from search API
export const mockDocuments: Document[] = [
  {
    id: "doc-001",
    title: "Attention Is All You Need",
    authors: ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar", "Jakob Uszkoreit", "Llion Jones", "Aidan N. Gomez", "Łukasz Kaiser", "Illia Polosukhin"],
    year: 2017,
    url: "https://arxiv.org/pdf/1706.03762.pdf",
    isPDF: true,
    summary: "Transformer architecture introduced, enabling parallelization and state-of-the-art results in translation and language modeling.",
  },
  {
    id: "doc-002",
    title: "BERT: Pre-training of Deep Bidirectional Transformers",
    authors: ["Jacob Devlin", "Ming-Wei Chang", "Kenton Lee", "Kristina Toutanova"],
    year: 2019,
    url: "https://arxiv.org/pdf/1810.04805.pdf",
    isPDF: true,
    summary: "Bidirectional encoder representations from transformers; achieves strong results on GLUE and SQuAD.",
  },
  {
    id: "doc-003",
    title: "Scaling Laws for Neural Language Models",
    authors: ["Jared Kaplan", "Sam McCandlish", "Tom Henighan", "Tom B. Brown", "Benjamin Chess", "Rewon Child", "Scott Gray", "Alec Radford", "Jeffrey Wu", "Dario Amodei"],
    year: 2020,
    url: "https://arxiv.org/pdf/2001.08361.pdf",
    isPDF: true,
    summary: "Empirical study of loss scaling with model size, dataset size, and compute.",
  },
];