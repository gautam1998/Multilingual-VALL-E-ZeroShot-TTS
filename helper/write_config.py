import yaml
import os

config_info = {'seed': 43,
               'dataset': {
                   "data_proportion": 0.05,
                   'test_size': 0.05,
                   'raw_train_path': "../../data/raw/train.txt",
                   'raw_test_path': "../../data/raw/test.txt",
                   'raw_dataset_dir': "../../data/raw/raw_dataset",
                   'processed_train_dir': "../../data/processed/processed_train",
                   'processed_test_dir': "../../data/processed/processed_test"
               },
               'tokenizer': {
                   'vocab_size': 30_522,
                   'max_length': 512,
                   'truncate_longer_samples': False,
                   'files': ["../../data/raw/test.txt"],
                   'tokenizer_path': "../../models/tokenizer",
                   'special_tokens': ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]", "<S>", "<T>"]
               },
               'bert': {
                   'hidden_size': 24,
                   'model_path': "../../models/exp02",
                   'mlm_probability': 0.15,
                   'evaluation_strategy': "epoch",
                   'num_train_epochs': 15,
                   # 'per_device_train_batch_size': 32,
                   'gradient_accumulation_steps': 8,
                   # 'per_device_eval_batch_size': 32,
                   "auto_find_batch_size": True,
                   'logging_steps': 100,
                   'save_strategy': "epoch",
                   'save_steps': 5000,
                   "learning_rate": 1e-04,
                   "weight_decay": 0.01,
                   "adam_beta1": 0.9,
                   "adam_beta2": 0.999,
                   "lr_scheduler_type": 'linear',
                   "warmup_ratio": 0.01,
                   "push_to_hub": False,
                   "hub_token": "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",
                   "hub_private_repo": True,
                   "hub_strategy": "checkpoint",
                   "hub_model_id": "gaushh/optimized-bert"
               }
               }

with open("../src/config/exp06.yaml", 'w') as yamlfile:
    data = yaml.dump(config_info, yamlfile)
    print("Write successful")