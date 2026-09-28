// Mirrors api/models.py — keep in sync with the backend.

export interface ImageResult {
  url: string;
  thumbnail: string;
  title: string;
  creator: string;
  source: string;
  license_code: string;
  license_url: string;
  requires_attribution: boolean;
  attribution: string;
  foreign_landing_url: string;
  matched_keyword: string;
  confidence: number;
}
