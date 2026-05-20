#!/bin/bash
# Surrogate-1 Quickstart Tutorial - 4-minute setup walkthrough

echo "🚀 Step 1: Clone repository"
git clone https://github.com/axentx/surrogate-1-training-pairs.git
cd surrogate-1-training-pairs || exit 1

echo "📦 Step 2: Install dependencies"
npm install -g @axentx/cli  # Global CLI tool
npm install                # Local project deps

echo "⚙️ Step 3: Configure environment"
cp .env.example .env       # Copy example env vars
sed -i 's/DUMMY_KEY=.*$/DUMMY_KEY=example/' .env  # Replace placeholder

echo "🧪 Step 4: Run first dataset slice"
axentx run --shard 0 --dataset demo  # Processes 1/16th of sample data

echo "✅ Done! Your first batch processed. Check ./output/demo-0 for results"