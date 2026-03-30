import { useState } from "react";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";
import ImageUpload from "@/components/ImageUpload";
import SubjectSelector from "@/components/SubjectSelector";
import ExplanationDisplay from "@/components/ExplanationDisplay";
import { analyzeExerciseImage, type GeminiResponse } from "@/lib/gemini";
import { toast } from "sonner";

const Index = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<GeminiResponse | null>(null);
  const [subject, setSubject] = useState("auto");

  const handleImageSelected = async (base64: string, mimeType: string) => {
    setIsLoading(true);
    setResult(null);
    try {
      const data = await analyzeExerciseImage(base64, mimeType, subject);
      setResult(data);
    } catch (err: any) {
      toast.error(err.message || "حصل خطأ. المرجو المحاولة مرة أخرى.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen gradient-hero">
      {/* Header */}
      <header className="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
        <div className="container max-w-lg mx-auto py-3 px-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-lg gradient-primary flex items-center justify-center">
              <span className="text-primary-foreground font-heading font-bold text-lg">م</span>
            </div>
            <div>
              <h1 className="font-heading font-bold text-foreground text-base leading-tight">مكنون OSTAD</h1>
              <p className="text-xs text-muted-foreground">أستاذك الذكي</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container max-w-lg mx-auto px-4 py-6 space-y-6">
        {/* Hero Section */}
        {!result && !isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center py-4"
          >
            <h2 className="font-heading text-2xl font-bold text-foreground mb-2">
              مرحباً بيك! 👋
            </h2>
            <p className="font-body text-muted-foreground leading-relaxed">
              صوّر التمرين ديالك وأنا نشرحو ليك بالدارجة بطريقة بسيطة
            </p>
          </motion.div>
        )}

        {/* Subject Selector */}
        {!result && !isLoading && (
          <SubjectSelector selected={subject} onSelect={setSubject} />
        )}

        {/* Upload Section */}
        <ImageUpload onImageSelected={handleImageSelected} isLoading={isLoading} />

        {/* Loading */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center gap-3 py-8"
          >
            <div className="w-14 h-14 rounded-full gradient-primary flex items-center justify-center animate-pulse-glow">
              <Loader2 className="w-7 h-7 text-primary-foreground animate-spin" />
            </div>
            <p className="font-heading font-semibold text-foreground">كنحلل التمرين...</p>
            <p className="text-sm text-muted-foreground">صبر شوية، الأستاذ كيقرا 📖</p>
          </motion.div>
        )}

        {/* Results */}
        {result && <ExplanationDisplay data={result} />}
      </main>

      {/* Footer */}
      <footer className="py-6 text-center">
        <p className="text-xs text-muted-foreground font-body">مكنون OSTAD © 2026 — أستاذك الذكي</p>
      </footer>
    </div>
  );
};

export default Index;
