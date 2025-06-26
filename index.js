const express = require("express");
const { S3Client, ListBucketsCommand } = require("@aws-sdk/client-s3");
const path = require("path");

const app = express();
const PORT = 3000;

const s3Client = new S3Client({
  region: "us-east-1", 
  credentials: {
    accessKeyId: "AKIAYKFQQ6EE3VYIEYFA",
    secretAccessKey: "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",
  },
});

const getBuckets = async () => {
  try {
    const data = await s3Client.send(new ListBucketsCommand({}));
    return data.Buckets || [];
  } catch (err) {
    console.error("Error fetching buckets", err);
    return [];
  }
};

app.use(express.static(path.join(__dirname, "public")));

app.get("/api/buckets", async (req, res) => {
  const buckets = await getBuckets();
  res.json(buckets);
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
