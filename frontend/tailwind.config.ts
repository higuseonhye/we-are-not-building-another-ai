import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17201b",
        paper: "#f6f3ea",
        moss: "#3f5f4a",
        rust: "#9d5a42",
        tide: "#2f6571",
        flax: "#d7c78d",
      },
      boxShadow: {
        soft: "0 18px 60px rgba(23, 32, 27, 0.10)",
      },
    },
  },
  plugins: [],
};

export default config;
