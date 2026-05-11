---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:363846
- loss:CosineSimilarityLoss
base_model: sentence-transformers/all-MiniLM-L6-v2
widget:
- source_sentence: How do I find my social security number online for free?
  sentences:
  - How can I earn a few dollars in just a week?
  - How can I get a copy of my social security number online?
  - How can I tell someone who has virtually no empathy that it really hurts that
    they don't show remorse or care in their language?
- source_sentence: '"How can I fix ""Error 105 (net::ERR_NAME_NOT_RESOLVED): The server
    could not be found."" on Chrome?"'
  sentences:
  - '"What is ""internal link stacking""?"'
  - '"How do you fix the ""no data received"" error on Chrome?"'
  - How do I stop my pet rat from biting me?
- source_sentence: How can you maximize your happiness in life?
  sentences:
  - Should I buy an iPhone 6 plus with a potential bending problem, or should I wait
    until Apple gives a genuine response?
  - In your opinion, what is the most fundamental skincare product you can use every
    day?
  - How do we sustain happiness in life?
- source_sentence: How can I reach Taj Mahal Hotel, Colaba from Mumbai Airport?
  sentences:
  - How can I reach Hinjewadi, Pune from Borivali, Mumbai?
  - Should I (a prospective Indian student) stop applying to universities in the USA,
    now that Donald Trump has become the president?
  - What are some good technology magazines to subscribe in India?
- source_sentence: How many marks should I get in JEE main paper 2 to get into NITs?
  sentences:
  - I have got 93% marks in 12th and 121 marks in Nata. I got 212 in Jee mains Paper
    2. Will I get NIT or any govt. colleges in Kerala?
  - Are there any moments in your life that you thought were insignificant at the
    time but ended up being very important in retrospect? If so, what are they?
  - How does Chinese military compare with the military capabilities of USSR?
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on sentence-transformers/all-MiniLM-L6-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). It maps sentences & paragraphs to a 384-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, text classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) <!-- at revision c9745ed1d9f207416be6d2e6f8de32d1f16199bf -->
- **Maximum Sequence Length:** 256 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'max_seq_length': 256, 'do_lower_case': False, 'architecture': 'BertModel'})
  (1): Pooling({'word_embedding_dimension': 384, 'pooling_mode_cls_token': False, 'pooling_mode_mean_tokens': True, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False, 'pooling_mode_weightedmean_tokens': False, 'pooling_mode_lasttoken': False, 'include_prompt': True})
  (2): Normalize()
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```

Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'How many marks should I get in JEE main paper 2 to get into NITs?',
    'I have got 93% marks in 12th and 121 marks in Nata. I got 212 in Jee mains Paper 2. Will I get NIT or any govt. colleges in Kerala?',
    'Are there any moments in your life that you thought were insignificant at the time but ended up being very important in retrospect? If so, what are they?',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[ 1.0000, -0.0168, -0.1096],
#         [-0.0168,  1.0000, -0.0872],
#         [-0.1096, -0.0872,  1.0000]])
```

<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 363,846 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>label</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                        | sentence_1                                                                        | label                                                          |
  |:--------|:----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------|
  | type    | string                                                                            | string                                                                            | float                                                          |
  | details | <ul><li>min: 6 tokens</li><li>mean: 15.69 tokens</li><li>max: 60 tokens</li></ul> | <ul><li>min: 6 tokens</li><li>mean: 15.51 tokens</li><li>max: 67 tokens</li></ul> | <ul><li>min: 0.0</li><li>mean: 0.37</li><li>max: 1.0</li></ul> |
* Samples:
  | sentence_0                                                        | sentence_1                                                                                     | label            |
  |:------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------|:-----------------|
  | <code>How many rounds are there in a Google interview?</code>     | <code>I ranked under 50 in Google Apac Test Round B. Should I expect an interview call?</code> | <code>0.0</code> |
  | <code>Is Quora becoming more or less like Facebook?</code>        | <code>Why is Quora becoming like Facebook?</code>                                              | <code>0.0</code> |
  | <code>Which is the most ancient civilization in the earth?</code> | <code>Which was the first civilization on earth?</code>                                        | <code>1.0</code> |
* Loss: [<code>CosineSimilarityLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#cosinesimilarityloss) with these parameters:
  ```json
  {
      "loss_fct": "torch.nn.modules.loss.MSELoss"
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 1
- `per_device_eval_batch_size`: 16
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 1
- `max_steps`: -1
- `learning_rate`: 5e-05
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_steps`: 0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `optim_target_modules`: None
- `gradient_accumulation_steps`: 1
- `average_tokens_across_devices`: True
- `max_grad_norm`: 1
- `label_smoothing_factor`: 0.0
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `use_cache`: False
- `neftune_noise_alpha`: None
- `torch_empty_cache_steps`: None
- `auto_find_batch_size`: False
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `include_num_input_tokens_seen`: no
- `log_level`: passive
- `log_level_replica`: warning
- `disable_tqdm`: False
- `project`: huggingface
- `trackio_space_id`: trackio
- `eval_strategy`: no
- `per_device_eval_batch_size`: 16
- `prediction_loss_only`: True
- `eval_on_start`: False
- `eval_do_concat_batches`: True
- `eval_use_gather_object`: False
- `eval_accumulation_steps`: None
- `include_for_metrics`: []
- `batch_eval_metrics`: False
- `save_only_model`: False
- `save_on_each_node`: False
- `enable_jit_checkpoint`: False
- `push_to_hub`: False
- `hub_private_repo`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_always_push`: False
- `hub_revision`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `restore_callback_states_from_checkpoint`: False
- `full_determinism`: False
- `seed`: 42
- `data_seed`: None
- `use_cpu`: False
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `dataloader_prefetch_factor`: None
- `remove_unused_columns`: True
- `label_names`: None
- `train_sampling_strategy`: random
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `ddp_backend`: None
- `ddp_timeout`: 1800
- `fsdp`: []
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `deepspeed`: None
- `debug`: []
- `skip_memory_metrics`: True
- `do_predict`: False
- `resume_from_checkpoint`: None
- `warmup_ratio`: None
- `local_rank`: -1
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Logs
| Epoch  | Step  | Training Loss |
|:------:|:-----:|:-------------:|
| 0.0220 | 500   | 0.1585        |
| 0.0440 | 1000  | 0.1397        |
| 0.0660 | 1500  | 0.1363        |
| 0.0879 | 2000  | 0.1337        |
| 0.1099 | 2500  | 0.1321        |
| 0.1319 | 3000  | 0.1282        |
| 0.1539 | 3500  | 0.1275        |
| 0.1759 | 4000  | 0.1271        |
| 0.1979 | 4500  | 0.1250        |
| 0.2199 | 5000  | 0.1254        |
| 0.2419 | 5500  | 0.1228        |
| 0.2638 | 6000  | 0.1227        |
| 0.2858 | 6500  | 0.1220        |
| 0.3078 | 7000  | 0.1155        |
| 0.3298 | 7500  | 0.1199        |
| 0.3518 | 8000  | 0.1160        |
| 0.3738 | 8500  | 0.1154        |
| 0.3958 | 9000  | 0.1202        |
| 0.4177 | 9500  | 0.1174        |
| 0.4397 | 10000 | 0.1132        |
| 0.4617 | 10500 | 0.1165        |
| 0.4837 | 11000 | 0.1146        |
| 0.5057 | 11500 | 0.1181        |
| 0.5277 | 12000 | 0.1122        |
| 0.5497 | 12500 | 0.1131        |
| 0.5717 | 13000 | 0.1120        |
| 0.5936 | 13500 | 0.1157        |
| 0.6156 | 14000 | 0.1115        |
| 0.6376 | 14500 | 0.1110        |
| 0.6596 | 15000 | 0.1111        |
| 0.6816 | 15500 | 0.1117        |
| 0.7036 | 16000 | 0.1090        |
| 0.7256 | 16500 | 0.1082        |
| 0.7475 | 17000 | 0.1099        |
| 0.7695 | 17500 | 0.1084        |
| 0.7915 | 18000 | 0.1109        |
| 0.8135 | 18500 | 0.1128        |
| 0.8355 | 19000 | 0.1138        |
| 0.8575 | 19500 | 0.1090        |
| 0.8795 | 20000 | 0.1095        |
| 0.9015 | 20500 | 0.1091        |
| 0.9234 | 21000 | 0.1075        |
| 0.9454 | 21500 | 0.1113        |
| 0.9674 | 22000 | 0.1103        |
| 0.9894 | 22500 | 0.1072        |


### Framework Versions
- Python: 3.14.3
- Sentence Transformers: 5.3.0
- Transformers: 5.4.0
- PyTorch: 2.11.0
- Accelerate: 1.13.0
- Datasets: 4.8.4
- Tokenizers: 0.22.2

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->