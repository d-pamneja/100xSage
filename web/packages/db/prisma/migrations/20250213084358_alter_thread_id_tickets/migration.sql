/*
  Warnings:

  - Changed the type of `thread_id` on the `Ticket` table. No cast exists, the column would be dropped and recreated, which cannot be done if there is data, since the column is required.

*/
-- AlterTable
ALTER TABLE "Ticket" DROP COLUMN "thread_id",
ADD COLUMN     "thread_id" INTEGER NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "Ticket_thread_id_key" ON "Ticket"("thread_id");
