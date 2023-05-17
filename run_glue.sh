
# include parse_yaml function
pip install -r requirements.txt
ls
source ./yaml_parser.sh

# model path should be same location as this shell file
#python src/glue/download_glue_data.py
export output_dir="output_glue"
export exp_name="exp03"
eval $(parse_yaml src/config/glue_config.yaml "config_")
mkdir $output_dir
mkdir $output_dir/$exp_name/
mkdir $output_dir/$exp_name/$config_task1_task_name
mkdir $output_dir/$exp_name/$config_task2_task_name
mkdir $output_dir/$exp_name/$config_task3_task_name
export path_to_models="models"
python src/glue/run_glue.py \
  --model_type $config_task1_model_type \
  --model_name_or_path $path_to_models/$exp_name/$config_task1_model_path \
  --task_name $config_task1_task_name \
  --do_train \
  --do_eval \
  --do_lower_case \
  --data_dir $config_task1_glue_dir/$config_task1_task_name/ \
  --max_seq_length $config_task1_max_seq_length \
  --per_gpu_train_batch_size $config_task1_per_gpu_train_batch_size \
  --learning_rate $config_task1_learning_rate \
  --num_train_epochs $config_task1_num_train_epochs \
  --output_dir $output_dir/$exp_name/$config_task1_task_name

python src/glue/run_glue.py \
  --model_type $config_task2_model_type \
  --model_name_or_path $path_to_models/$exp_name/$config_task2_model_path \
  --task_name $config_task2_task_name \
  --do_train \
  --do_eval \
  --do_lower_case \
  --data_dir $config_task2_glue_dir/$config_task2_task_name/ \
  --max_seq_length $config_task2_max_seq_length \
  --per_gpu_train_batch_size $config_task2_per_gpu_train_batch_size \
  --learning_rate $config_task2_learning_rate \
  --num_train_epochs $config_task2_num_train_epochs \
  --output_dir $output_dir/$exp_name/$config_task2_task_name

python src/glue/run_glue.py \
  --model_type $config_task3_model_type \
  --model_name_or_path $path_to_models/$exp_name/$config_task3_model_path \
  --task_name $config_task3_task_name \
  --do_train \
  --do_eval \
  --do_lower_case \
  --data_dir $config_task3_glue_dir/$config_task3_task_name/ \
  --max_seq_length $config_task3_max_seq_length \
  --per_gpu_train_batch_size $config_task3_per_gpu_train_batch_size \
  --learning_rate $config_task3_learning_rate \
  --num_train_epochs $config_task3_num_train_epochs \
  --output_dir $output_dir/$exp_name/$config_task3_task_name

