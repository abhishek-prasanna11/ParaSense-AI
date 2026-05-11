import { useState } from "react";
import { motion } from "framer-motion";
import {
  Search,
  Repeat,
  Network,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [text1, setText1] = useState("");
  const [text2, setText2] = useState("");

  const navigate = useNavigate();

  const handleAnalyze = () => {
    if (!text1 || !text2) return;

    setLoading(true);

    setTimeout(() => {
      navigate("/result", {
        state: {
          text1,
          text2,
        },
      });
    }, 800);
  };

  return (
    <div className="min-h-screen w-full text-gray-300 font-sans flex gap-6 px-6">
      {/* Background Glow */}
      <div className="absolute top-0 left-0 w-full h-full pointer-events-none">
        <div className="absolute top-[-15%] left-[-5%] w-[60%] h-[60%] bg-blue-600/5 blur-[140px] rounded-full" />
        <div className="absolute bottom-[-15%] right-[-5%] w-[60%] h-[60%] bg-indigo-600/5 blur-[140px] rounded-full" />
      </div>

      {/* Sidebar */}
      <motion.div
        initial={{ x: -60, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        className="w-[420px] xl:w-[480px] border-r border-white/5 bg-black/30 backdrop-blur-3xl px-12 py-12 flex flex-col justify-between relative z-10"
      >
        <div>
          <div className="flex items-center gap-3 text-blue-500 mb-10">
            <div className="p-2.5 bg-blue-500/10 rounded-xl border border-blue-500/20">
              <Network size={22} />
            </div>
            <span className="font-black tracking-widest text-lg text-white">
              ParaSense AI
            </span>
          </div>

          <h1 className="text-4xl font-black text-white mb-8">
            Semantic <br />
            <span className="bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
              Transformer
            </span>
          </h1>

          <div className="space-y-6 text-sm text-gray-400 leading-relaxed">

            {/* Model */}
            <section>
              <h3 className="text-white font-semibold mb-1">Model</h3>
              <p>
                Uses <span className="text-gray-200">all-mpnet-base-v2 (SBERT)</span> for
                high-quality semantic understanding and better handling of nuanced language.
              </p>
            </section>

            {/* Training */}
            <section>
              <h3 className="text-white font-semibold mb-1">Training</h3>
              <p>
                Trained with <span className="text-gray-200">Contrastive Loss</span> and
                custom hard-negative samples to improve handling of negation and tricky cases.
              </p>
            </section>

            {/* Dataset */}
            <section>
              <h3 className="text-white font-semibold mb-1">Dataset</h3>
              <p>
                Fine-tuned on <span className="text-gray-200">Quora Question Pairs</span> using
                a curated subset of high-quality examples.
              </p>
            </section>

            {/* Output */}
            <section>
              <h3 className="text-white font-semibold mb-1">Output</h3>
              <p>
                Computes cosine similarity with a <span className="text-gray-200">0.75 threshold</span>
                to classify paraphrases accurately.
              </p>
            </section>

          </div>
        </div>
      </motion.div>

      {/* Main */}
     <main className="flex-1 pl-24 pr-20 py-16 flex flex-col relative z-10 min-h-screen">
        {/* Header */}
        <header className="mb-12 border-b border-white/5 pb-6">
          <h2 className="text-white text-lg font-semibold">
            Semantic Analysis Engine
          </h2>
        </header>

        {/* Intro */}
        <div className="max-w-3xl mb-12 space-y-4">
          <p className="text-gray-300 text-sm">
            Compare two sentences and automatically compute both their semantic
            similarity score and whether they are paraphrases.
          </p>

          <div className="bg-white/[0.03] border border-white/10 rounded-xl p-5 text-sm text-gray-400">
            <p className="text-white font-semibold mb-2">How to use:</p>
            <ul className="space-y-2">
              <li>• Enter two sentences</li>
              <li>• Click Analyze</li>
              <li>• View similarity score and paraphrase result</li>
            </ul>
          </div>
        </div>

        {/* Inputs */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input 1 */}
          <div className="relative">
            <textarea
              value={text1}
              onChange={(e) => setText1(e.target.value)}
              placeholder="Enter first sentence..."
              className="w-full h-48 p-8 bg-white/[0.03] border border-white/10 rounded-2xl text-white placeholder:text-gray-600 resize-none"
            />
          </div>

          {/* Input 2 */}
          <div className="relative">
            <textarea
              value={text2}
              onChange={(e) => setText2(e.target.value)}
              placeholder="Enter second sentence..."
              className="w-full h-48 p-8 bg-white/[0.03] border border-white/10 rounded-2xl text-white placeholder:text-gray-600 resize-none"
            />

            {/* Swap Button */}
            <button
              onClick={() => {
                setText1(text2);
                setText2(text1);
              }}
              className="absolute top-1/2 -left-6 -translate-y-1/2 p-3 bg-white text-black rounded-full shadow-md"
            >
              <Repeat size={18} />
            </button>
          </div>
        </div>

        {/* Analyze Button */}
        <button
          onClick={handleAnalyze}
          className="mt-10 h-20 bg-white text-black rounded-2xl text-xl font-bold flex items-center justify-center gap-3"
        >
          {loading ? "Processing..." : "Analyze"}
          <Search size={22} />
        </button>
      </main>
    </div>
  );
}
