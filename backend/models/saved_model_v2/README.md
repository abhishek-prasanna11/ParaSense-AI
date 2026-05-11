---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:56515
- loss:ContrastiveLoss
base_model: sentence-transformers/all-mpnet-base-v2
widget:
- source_sentence: well that that certainly can happen now if you you say you're in
    communications uh what base of communications would you be most interested in
    getting in to
  sentences:
  - How do I buy stock?
  - What will be your new year resolution for 2017 and your plan of execution?
  - 'What base of communications are you most interested in? '
- source_sentence: Why people tend to yell when they're drunk?
  sentences:
  - What are the environmental impacts of the tourism industry and how does it negatively
    impacted Rome?
  - Cleveland kidnapper Ariel Castro found hanging in his cell
  - Are people more willing to talk to me if they've drunk some alcohol?
- source_sentence: Don Diego de San Francisco Tehuetzquititzin ( sometimes called
    Tehuetzquiti or Tehuetzqui ) ( died 1554 ) was the 16th `` tlatoani '' and second
    governor of Tenochtitlan .
  sentences:
  - Which intersections in London, ON are particularly dangerous? Why? What could
    be done to improve them?
  - Don Diego de San Francisco Tehuetzquititzin ( sometimes called Tehuetzquiti or
    Tehuetzqui ) ( died 1554 ) was the 16th `` tlatoani '' and the second governor
    of Tenochtitlan .
  - 'Break a leg. '
- source_sentence: What does someone like you have to do in your spare time?
  sentences:
  - What would you like to do in your spare time?
  - What are some unexpected things first-time visitors to China notice?
  - How can you check your Axis Bank account balance online?
- source_sentence: In 1915 , Pando and a number of dissatisfied liberals and former
    conservatives formed the Republican Party .
  sentences:
  - Collective bargaining will restrict doctors' ability to prescribe quality medicine
    for their patients.
  - In 1915 , Pando and a number of discontented Liberals and former Conservatives
    formed the Republican Party .
  - If there's infinite energy in zero point energy and infinite virtual particles
    in vacuum energy, is this real or just a mathematical thing?
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on sentence-transformers/all-mpnet-base-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2). It maps sentences & paragraphs to a 768-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, text classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) <!-- at revision e8c3b32edf5434bc2275fc9bab85f82640a19130 -->
- **Maximum Sequence Length:** 384 tokens
- **Output Dimensionality:** 768 dimensions
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
  (0): Transformer({'max_seq_length': 384, 'do_lower_case': False, 'architecture': 'MPNetModel'})
  (1): Pooling({'word_embedding_dimension': 768, 'pooling_mode_cls_token': False, 'pooling_mode_mean_tokens': True, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False, 'pooling_mode_weightedmean_tokens': False, 'pooling_mode_lasttoken': False, 'include_prompt': True})
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
    'In 1915 , Pando and a number of dissatisfied liberals and former conservatives formed the Republican Party .',
    'In 1915 , Pando and a number of discontented Liberals and former Conservatives formed the Republican Party .',
    "If there's infinite energy in zero point energy and infinite virtual particles in vacuum energy, is this real or just a mathematical thing?",
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 768]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.9014, 0.1098],
#         [0.9014, 1.0000, 0.0845],
#         [0.1098, 0.0845, 1.0000]])
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

* Size: 56,515 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>label</code>
* Approximate statistics based on the first 1000 samples:
  |         | sentence_0                                                                        | sentence_1                                                                        | label                                                          |
  |:--------|:----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------|
  | type    | string                                                                            | string                                                                            | float                                                          |
  | details | <ul><li>min: 5 tokens</li><li>mean: 19.05 tokens</li><li>max: 96 tokens</li></ul> | <ul><li>min: 5 tokens</li><li>mean: 17.73 tokens</li><li>max: 61 tokens</li></ul> | <ul><li>min: 0.0</li><li>mean: 0.45</li><li>max: 1.0</li></ul> |
* Samples:
  | sentence_0                                                                                                                                                                               | sentence_1                                                                                                                                          | label            |
  |:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------|
  | <code>Buy amazon prime uk with gift card?</code>                                                                                                                                         | <code>What is the connection between fear and acohol/drug addiction?</code>                                                                         | <code>0.0</code> |
  | <code>The arena has hosted concerts by many famous artists , including Whitney Houston , André Rieu , TOTO , Trance Energy and Tina Turner , among others .</code>                       | <code>The Arena has hosted concerts by many famous artists , including Whitney Houston , Tina Turner , TOTO , Trance Energy and André Rieu .</code> | <code>1.0</code> |
  | <code>GAO's work, the Congress reduced the fiscal year 1999 military personnel budget for active and reserve forces by about $609 million without compromising overall readiness.</code> | <code>The congress reduced the military personnel budget without compromising readiness. </code>                                                    | <code>1.0</code> |
* Loss: [<code>ContrastiveLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#contrastiveloss) with these parameters:
  ```json
  {
      "distance_metric": "SiameseDistanceMetric.COSINE_DISTANCE",
      "margin": 0.5,
      "size_average": true
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `num_train_epochs`: 1
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 8
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
- `per_device_eval_batch_size`: 8
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
| Epoch  | Step | Training Loss |
|:------:|:----:|:-------------:|
| 0.0708 | 500  | 0.0242        |
| 0.1415 | 1000 | 0.0202        |
| 0.2123 | 1500 | 0.0185        |
| 0.2831 | 2000 | 0.0178        |
| 0.3539 | 2500 | 0.0176        |
| 0.4246 | 3000 | 0.0171        |
| 0.4954 | 3500 | 0.0167        |
| 0.5662 | 4000 | 0.0168        |
| 0.6369 | 4500 | 0.0162        |
| 0.7077 | 5000 | 0.0162        |
| 0.7785 | 5500 | 0.0164        |
| 0.8493 | 6000 | 0.0153        |
| 0.9200 | 6500 | 0.0155        |
| 0.9908 | 7000 | 0.0157        |


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

#### ContrastiveLoss
```bibtex
@inproceedings{hadsell2006dimensionality,
    author={Hadsell, R. and Chopra, S. and LeCun, Y.},
    booktitle={2006 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR'06)},
    title={Dimensionality Reduction by Learning an Invariant Mapping},
    year={2006},
    volume={2},
    number={},
    pages={1735-1742},
    doi={10.1109/CVPR.2006.100}
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