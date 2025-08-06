# OpenAI Model Cost Guide

## Model Pricing (as of 2024)

| Model         | Input Cost       | Output Cost      | Best For                       |
| ------------- | ---------------- | ---------------- | ------------------------------ |
| GPT-4o        | $5.00/1M tokens  | $15.00/1M tokens | Complex analysis, high quality |
| GPT-4o Mini   | $0.15/1M tokens  | $0.60/1M tokens  | **Cost-effective analysis**    |
| GPT-4 Turbo   | $10.00/1M tokens | $30.00/1M tokens | Legacy GPT-4                   |
| GPT-3.5 Turbo | $0.50/1M tokens  | $1.50/1M tokens  | Basic tasks                    |

## Cost Analysis for Podcast Transcripts

### Typical 1-Hour Podcast

- **Input**: ~10,000 words ≈ 13,000 tokens
- **Output**: ~2,000 words ≈ 2,600 tokens

### Cost per Transcript

- **GPT-4o**: ~$0.07 + $0.04 = **$0.11**
- **GPT-4o Mini**: ~$0.002 + $0.002 = **$0.004** ⭐
- **GPT-3.5 Turbo**: ~$0.007 + $0.004 = **$0.011**

## Recommendations

### For Most Users: GPT-4o Mini

- **Cost**: ~$0.004 per transcript
- **Quality**: Excellent for podcast analysis
- **Speed**: Fast responses
- **Value**: Best price/performance ratio

### For High-Quality Analysis: GPT-4o

- **Cost**: ~$0.11 per transcript
- **Quality**: Highest quality analysis
- **Use Case**: Important podcasts, detailed analysis needed

### For Budget Users: GPT-3.5 Turbo

- **Cost**: ~$0.011 per transcript
- **Quality**: Good for basic analysis
- **Use Case**: When cost is primary concern

## Usage Examples

```bash
# Use default (GPT-4o Mini) - recommended
deepcast transcript.txt

# Use GPT-4o for high-quality analysis
deepcast transcript.txt --model gpt-4o

# Use GPT-3.5 Turbo for budget option
deepcast transcript.txt --model gpt-3.5-turbo

# Set model in .env file
echo "OPENAI_MODEL=gpt-4o-mini" >> .env
```

## Monthly Cost Estimates

| Transcripts/Month | GPT-4o Mini | GPT-4o | GPT-3.5 Turbo |
| ----------------- | ----------- | ------ | ------------- |
| 10                | $0.04       | $1.10  | $0.11         |
| 50                | $0.20       | $5.50  | $0.55         |
| 100               | $0.40       | $11.00 | $1.10         |
| 500               | $2.00       | $55.00 | $5.50         |

## Tips to Reduce Costs

1. **Use GPT-4o Mini** as default (already configured)
2. **Batch process** multiple transcripts
3. **Optimize prompts** to reduce output length
4. **Monitor usage** in OpenAI dashboard
5. **Set spending limits** in OpenAI account

## Model Comparison for Podcast Analysis

| Aspect                | GPT-4o Mini | GPT-4o     | GPT-3.5 Turbo |
| --------------------- | ----------- | ---------- | ------------- |
| **Cost**              | ⭐⭐⭐⭐⭐  | ⭐⭐       | ⭐⭐⭐⭐      |
| **Quality**           | ⭐⭐⭐⭐    | ⭐⭐⭐⭐⭐ | ⭐⭐⭐        |
| **Speed**             | ⭐⭐⭐⭐⭐  | ⭐⭐⭐     | ⭐⭐⭐⭐      |
| **Analysis Depth**    | ⭐⭐⭐⭐    | ⭐⭐⭐⭐⭐ | ⭐⭐⭐        |
| **Quote Extraction**  | ⭐⭐⭐⭐    | ⭐⭐⭐⭐⭐ | ⭐⭐⭐        |
| **Thematic Analysis** | ⭐⭐⭐⭐    | ⭐⭐⭐⭐⭐ | ⭐⭐⭐        |

**Recommendation**: Start with GPT-4o Mini for most use cases. Upgrade to GPT-4o only for critical analysis where the highest quality is needed.
