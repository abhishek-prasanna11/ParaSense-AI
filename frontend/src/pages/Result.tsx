import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";

type ResultData = {
  similarity: number;
  paraphrase: boolean;
};

export default function Result() {
  const location = useLocation();
  const navigate = useNavigate();
  const { text1, text2 } = location.state || {};

  const [data, setData] = useState<ResultData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Use relative URL so it works through both docker-compose (nginx proxy) and K8s Ingress
  // Forced rebuild commit
  const API_URL = "/api";

  useEffect(() => {
    const fetchResult = async () => {
      if (!text1 || !text2) {
        setError("Missing input text");
        setLoading(false);
        return;
      }

      try {
        const res = await axios.post(`${API_URL}/analyze`, {
          text1,
          text2,
        });

        console.log("API response:", res.data);
        setData(res.data);
      } catch (err: unknown) {
        console.error("API Error:", err);
        setError("Failed to fetch result. Check backend/CORS.");
      } finally {
        setLoading(false);
      }
    };

    fetchResult();
  }, [text1, text2]);

  return (
    <div className="min-h-screen bg-[#030304] text-white flex items-center justify-center p-6">
      <div className="w-full max-w-3xl bg-white/[0.03] border border-white/10 backdrop-blur-xl rounded-3xl p-10 shadow-2xl">

        {/* Header */}
        <h1 className="text-3xl font-bold mb-6 text-center">
          🔍 ParaSense AI Result
        </h1>

        {/* Input Display */}
        <div className="space-y-4 mb-8 text-sm text-gray-400">
          <div>
            <p className="text-gray-500">Sentence 1</p>
            <p className="text-white">{text1}</p>
          </div>

          <div>
            <p className="text-gray-500">Sentence 2</p>
            <p className="text-white">{text2}</p>
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className="flex justify-center items-center py-10">
            <div className="w-10 h-10 border-4 border-white border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="text-red-400 text-center py-4">
            {error}
          </div>
        )}

        {/* Result */}
        {data && !loading && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6 p-8 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl text-white flex flex-col items-center gap-6"
          >
            {/* Similarity */}
            <div className="text-center">
              <p className="text-sm opacity-70">Similarity Score</p>
              <h2 className="text-6xl font-bold">
                {(data.similarity * 100).toFixed(0)}%
              </h2>
            </div>

            {/* Divider */}
            <div className="w-full h-[1px] bg-white/20" />

            {/* Paraphrase */}
            <div className="text-center">
              <p className="text-sm opacity-70">Paraphrase</p>
              <h2 className="text-2xl font-semibold">
                {data.paraphrase
                  ? "Yes, both sentences are semantically similar"
                  : "No, the sentences are different"}
              </h2>
            </div>

            {/* Button */}
            <button
              onClick={() => navigate("/")}
              className="mt-6 px-6 py-3 bg-white text-black font-semibold rounded-full hover:bg-gray-200 transition-colors"
            >
              Home
            </button>
          </motion.div>
        )}
      </div>
    </div>
  );
}
