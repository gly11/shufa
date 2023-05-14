import matplotlib.pyplot as plt
# import build_dataset
import load_data
dataset_name = load_data.dataset_name


def plot(history, model_name, epoch, lr):
    acc = [0.] + history.history['accuracy']
    val_acc = [0.] + history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    plt.figure(figsize=(8, 8))
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Training Accuracy')
    plt.plot(val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.ylabel('Accuracy')
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.ylabel('Categorical Cross Entropy')
    plt.title('Training and Validation Loss')
    plt.xlabel('epoch')

    plt.suptitle(f"{model_name} with dataset:{dataset_name}, EPOCH = {epoch}, "
                 f"learning rate = {lr}")
    plt.savefig('{}/fig.png'.format(model_name), dpi=300, bbox_inches='tight')
    plt.savefig('{}/fig.eps'.format(model_name))
    plt.show()

    # 绘制训练 & 验证的准确率值