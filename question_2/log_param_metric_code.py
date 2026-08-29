
# Hyperparameters Logged 
mlflow.log_param("hidden_layer_sizes", str(hidden_layer_sizes))
mlflow.log_param("learning_rate_init", learning_rate_init)
mlflow.log_param("batch_size", batch_size)
mlflow.log_param("max_iter", max_iter)
mlflow.log_param("solver", "adam")
mlflow.log_param("activation", "relu")
# Metrics Logged 
mlflow.log_metric("train_loss", train_loss)
mlflow.log_metric("val_loss", val_loss)
mlflow.log_metric("val_accuracy", val_acc)
mlflow.log_metric("val_f1_macro", val_f1)



