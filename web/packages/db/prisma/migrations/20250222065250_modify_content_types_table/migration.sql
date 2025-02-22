/*
  Warnings:

  - Added the required column `topic_id` to the `Content` table without a default value. This is not possible if the table is not empty.
  - Added the required column `type_id` to the `Content` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Content" ADD COLUMN     "topic_id" INTEGER NOT NULL,
ADD COLUMN     "type_id" INTEGER NOT NULL;

-- CreateTable
CREATE TABLE "ContentType" (
    "id" SERIAL NOT NULL,
    "title" VARCHAR(50) NOT NULL,
    "description" VARCHAR(200) NOT NULL,

    CONSTRAINT "ContentType_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Content" ADD CONSTRAINT "Content_topic_id_fkey" FOREIGN KEY ("topic_id") REFERENCES "Topic"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Content" ADD CONSTRAINT "Content_type_id_fkey" FOREIGN KEY ("type_id") REFERENCES "ContentType"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
