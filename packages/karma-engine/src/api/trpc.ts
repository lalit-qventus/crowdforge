import { initTRPC } from "@trpc/server";
import superjson from "superjson";
import type { Db } from "../db/connection.js";

export interface KarmaContext {
  db: Db;
}

const t = initTRPC.context<KarmaContext>().create({
  transformer: superjson,
});

export const router = t.router;
export const publicProcedure = t.procedure;
