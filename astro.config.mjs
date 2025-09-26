// @ts-check
import { defineConfig } from "astro/config";

// https://astro.build/config
export default defineConfig({
  site: "https://neptunethefox.github.io",
  vite: {
    ssr: {
      noExternal: ["7.css"],
    },
  },
  output: "static",
});
