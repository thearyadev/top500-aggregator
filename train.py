import os

import numpy as np
from rich import print
from rich.live import Live
from rich.prompt import Prompt
from rich.table import Table

from neural_network import (
    Accuracy_Categorical,
    Activation_ReLU,
    Activation_Softmax,
    Layer_Dense,
    Loss_CategoricalCrossentropy,
    Model,
    Optimizer_Adam,
    create_data_mnist,
)


def train(
    dataset: tuple, epochs: int, batch_size: int, table: Table
) -> tuple[Model, list[tuple[int | float]]]:
    """Training proxy script for the neural network

    Args:
        dataset (tuple): all image dataset for mnist
        epochs (int): number of epochs to train for
        batch_size (int): batch size
        table (Table): display table

    Returns:
        tuple[Model, list[tuple[int | float]]]: model and training results
    """
    X, y, X_test, y_test = dataset  # unpack dataset

    # Shuffle the training dataset
    keys = np.array(range(X.shape[0]))
    np.random.shuffle(keys)
    X = X[keys]
    y = y[keys]

    # Scale and reshape samples
    X = (X.reshape(X.shape[0], -1).astype(np.float32) - 127.5) / 127.5
    X_test = (X_test.reshape(X_test.shape[0], -1).astype(np.float32) - 127.5) / 127.5

    # Instantiate the model
    model = Model()

    # Add layers
    model.add(Layer_Dense(X.shape[1], 128))
    model.add(Activation_ReLU())
    model.add(Layer_Dense(128, 128))
    model.add(Activation_ReLU())
    model.add(Layer_Dense(128, 38))
    model.add(Activation_Softmax())

    # Set loss, optimizer and accuracy objects
    model.set(
        loss=Loss_CategoricalCrossentropy(),
        optimizer=Optimizer_Adam(decay=1e-3),
        accuracy=Accuracy_Categorical(),
    )

    # Finalize the model
    model.finalize()

    # Train the model
    training_results = model.train(
        X,
        y,
        validation_data=(X_test, y_test),
        epochs=epochs,
        batch_size=batch_size,
        print_every=100,
        table=table,  # table is used to make a live table of the training results
    )

    return model, training_results  # return the model and training results


def write(
    model: Model,
    model_name: str,
    model_description: str,
    training_results: list[tuple[int | float]],
) -> None:
    """Writes model, params, and training results to disk

    Args:
        model (Model): NN model
        model_name (str): filesystem name
        model_description (str): description of the model
        training_results (list[tuple[int  |  float]]): training results

    Returns:
        _type_: None
    """
    model.save_parameters(f"models/{model_name}/{model_name}.params")
    model.save(f"models/{model_name}/{model_name}.model")
    with open(f"models/{model_name}/model_description", "w+") as f:
        f.write(model_description + "\n")
        f.write(
            f"{('Epoch #','Accuracy','Loss','Data Loss','Regularization Loss','Learning Rate')}\n"
        )
        for i in training_results:
            f.write(f"{i}\n")
    return None


def main():
    print("[yellow]Top 500 Aggregator Neural Network Training Tool")
    training_dataset_path = Prompt.ask(
        "[cyan]Enter the path to the training dataset",
        default="assets/top_500_mnist_images",
    )
    dataset = create_data_mnist(training_dataset_path)
    print(
        f"[green]Training dataset loaded. Training dataset shape: "
        f"{dict({'X Train': dataset[0].shape, 'Y Train': dataset[1].shape, 'X Test': dataset[2].shape, 'Y Test': dataset[3].shape})}"
    )
    model_name = Prompt.ask("[cyan]Enter the name of the model")
    if os.path.exists(f"models/{model_name}"):
        if (
            Prompt.ask(
                "[pink]Model already exists. Do you want to overwrite it?",
                choices=["y", "n"],
            )
            == "n"
        ):
            print("[green]Training cancelled")
            return
    model_description = Prompt.ask("[cyan]Enter the description of the model")
    epochs: int = int(Prompt.ask("[cyan]Enter the number of epochs", default="10"))
    batch_size: int = int(Prompt.ask("[cyan]Enter the batch size", default="128"))
    Prompt.ask("[cyan]Press enter to start training")

    table = Table(
        "Epoch #",
        "Accuracy",
        "Loss",
        "Data Loss",
        "Regularization Loss",
        "Learning Rate",
        title="Training Progress",
    )
    with Live(table, refresh_per_second=4):
        model, training_results = train(
            dataset=dataset, epochs=epochs, batch_size=batch_size, table=table
        )

    print("[green]Training complete")
    if Prompt.ask("[cyan]Do you want to save the model?", choices=["y", "n"]) == "y":
        write(
            model=model,
            model_name=model_name,
            model_description=model_description,
            training_results=training_results,
        )
        print("[green]Model saved in " + f"models/{model_name}/{model_name}.model")


if __name__ == "__main__":
    main()
