export type Requirement = {
  kind: "prerequisite" | "corequisite" | "combined" | "exclusion" | "crosslisting" | "historical" | "note";
  label: string;
  text: string;
  references: (string)[];
  logic: "source-text-only";
};

export type Variant = {
  pid: string;
  title: string;
  language: string | null;
  sourceIdentifier: string;
  sourceUrl: string;
};

export type Course = {
  id: string;
  subject: string;
  faculty: string;
  number: string;
  title: string;
  credits: string | null;
  description: string;
  requirements: (Requirement)[];
  detailStatus: "retrieved" | "index-only" | "unresolved";
  calendar: string;
  checkedAt: string | null;
  sourceUrl: string | null;
  variants?: (Variant)[];
  language?: string | null;
  requirementStatus?: string;
  isLassondeCatalog?: boolean;
  extractionWarnings?: (string)[];
};

export type Mention = {
  sheet: string;
  cell: string;
  text: string;
  context: string;
  courseIds: (string)[];
  yearHeading: string | null;
};

export type CurriculumGroup = {
  sheet: string;
  cell: string;
  yearHeading: string | null;
  text: string;
  courseIds: (string)[];
  kind: string;
  reviewStatus: string;
};

export type Program = {
  id: string;
  label: string;
  calendar: string;
  kind: "program" | "planning-aid";
  status: string;
  sourceUrl: string;
  courseIds: (string)[];
  checkedAt: string | null;
  mentions: (Mention)[];
  entryCourseIds?: (string)[];
  groups?: (CurriculumGroup)[];
  calendarInWorkbook?: boolean;
};

export type Edge = {
  source: string;
  target: string;
  kind: "prerequisite" | "corequisite" | "combined";
  section: number;
};

export type Graph = {
  nodes: (Course)[];
  edges: (Edge)[];
  total: number;
  semantics: string;
};

export type Failure = {
  source: string;
  error: string;
};

export type Coverage = {
  lassondeIndexed: number;
  lassondeDetails: number;
  supportingCourses: number;
  unresolvedReferences: number;
  programsExtracted: number;
  programsLinked: number;
  subjects: (string)[];
  failures: (Failure)[];
};

export type Meta = {
  schemaVersion: "1";
  calendar: string;
  generatedAt: string;
  sourceUrl: string;
  limitations: (string)[];
  coverage: Coverage;
};

export type Error = {
  error: string;
};
