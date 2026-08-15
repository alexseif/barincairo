import { GET as llmGet } from "../llm.txt/route";

export async function GET() {
  return llmGet();
}
