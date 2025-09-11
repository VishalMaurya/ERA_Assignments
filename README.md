# Session 4: Basic Neural Networks

## 🧠 Introduction to Neural Networks

Welcome to Session 4 of the ERA V4 course! This session focuses on building and understanding basic neural networks from scratch.

## 📚 Learning Objectives

By the end of this session, you will understand:

- **Fundamentals of Neural Networks**
  - Perceptrons and Multi-layer Perceptrons
  - Activation functions (ReLU, Sigmoid, Tanh)
  - Forward propagation
  - Backpropagation algorithm
  - Gradient descent optimization

- **Mathematical Foundations**
  - Linear algebra in neural networks
  - Matrix operations and vectorization
  - Chain rule for derivatives
  - Loss functions (MSE, Cross-entropy)

- **Implementation from Scratch**
  - Building a basic neural network without frameworks
  - Understanding weight initialization
  - Implementing gradient descent
  - Training and validation loops

## 🎯 Session Goals

### Core Implementations
- [ ] Build a simple perceptron
- [ ] Implement a multi-layer neural network from scratch
- [ ] Create different activation functions
- [ ] Implement forward and backward propagation
- [ ] Build a training loop with gradient descent

### Practical Applications
- [ ] Binary classification problem
- [ ] Multi-class classification
- [ ] Regression task
- [ ] XOR problem solving
- [ ] Basic image classification (MNIST digits)

## 🛠️ Technical Stack

- **Language**: Python 3.8+
- **Core Libraries**: 
  - NumPy (for mathematical operations)
  - Matplotlib (for visualization)
  - Pandas (for data handling)
- **Optional**: 
  - Jupyter Notebooks (for interactive development)
  - Seaborn (for advanced plotting)

## 📂 Project Structure

```
session-4-basic-NN/
├── README.md                 # This file
├── notebooks/               # Jupyter notebooks for experiments
│   ├── 01_perceptron.ipynb
│   ├── 02_mlp_scratch.ipynb
│   └── 03_applications.ipynb
├── src/                     # Source code
│   ├── neural_network.py   # Core NN implementation
│   ├── activations.py       # Activation functions
│   ├── optimizers.py        # Gradient descent variants
│   └── utils.py            # Helper functions
├── data/                    # Datasets
├── experiments/             # Training experiments
└── requirements.txt         # Dependencies
```

## 🚀 Getting Started

### Prerequisites

```bash
# Create virtual environment
python -m venv nn_env
source nn_env/bin/activate  # On Windows: nn_env\Scripts\activate

# Install dependencies
pip install numpy matplotlib pandas jupyter
```

### Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd session-4-basic-NN
   pip install -r requirements.txt
   ```

2. **Start with Perceptron**
   ```python
   from src.neural_network import Perceptron
   
   # Create and train a simple perceptron
   perceptron = Perceptron(input_size=2)
   perceptron.train(X_train, y_train, epochs=100)
   ```

3. **Build Multi-layer Network**
   ```python
   from src.neural_network import MLP
   
   # Create a 2-layer neural network
   model = MLP(layers=[784, 128, 10])
   model.train(X_train, y_train, epochs=50)
   ```

## 📊 Key Concepts Covered

### 1. **The Perceptron**
- Single neuron with linear decision boundary
- Binary classification capability
- Limitations and the XOR problem

### 2. **Multi-layer Perceptron (MLP)**
- Hidden layers for non-linear decision boundaries
- Universal approximation theorem
- Architecture design principles

### 3. **Activation Functions**
- **Sigmoid**: `σ(x) = 1/(1 + e^(-x))`
- **ReLU**: `f(x) = max(0, x)`
- **Tanh**: `tanh(x) = (e^x - e^(-x))/(e^x + e^(-x))`

### 4. **Training Process**
- Forward propagation: Computing outputs
- Loss calculation: Measuring errors
- Backpropagation: Computing gradients
- Parameter updates: Gradient descent

### 5. **Mathematical Foundations**
```
Forward Pass:
z^[l] = W^[l] * a^[l-1] + b^[l]
a^[l] = g(z^[l])

Backward Pass:
dW^[l] = (1/m) * dz^[l] * a^[l-1]^T
db^[l] = (1/m) * sum(dz^[l])
```

## 🎯 Assignments & Exercises

### Assignment 1: Perceptron Implementation
- Implement a perceptron from scratch
- Train on linearly separable data
- Visualize decision boundary

### Assignment 2: XOR Problem
- Demonstrate perceptron limitations
- Solve using multi-layer network
- Compare single vs multi-layer performance

### Assignment 3: MNIST Classification
- Build MLP for digit recognition
- Experiment with different architectures
- Analyze performance metrics

## 📈 Performance Metrics

Track these metrics during training:
- **Accuracy**: Percentage of correct predictions
- **Loss**: Training and validation loss curves
- **Convergence**: Epochs to reach target accuracy
- **Generalization**: Training vs validation performance

## 🔍 Debugging & Troubleshooting

### Common Issues:
1. **Vanishing Gradients**: Use ReLU activation
2. **Exploding Gradients**: Implement gradient clipping
3. **Overfitting**: Add regularization or early stopping
4. **Slow Convergence**: Adjust learning rate
5. **Poor Performance**: Check data preprocessing

### Debugging Tools:
- Gradient checking for backpropagation
- Loss curve visualization
- Weight histogram analysis
- Activation distribution monitoring

## 📚 Additional Resources

### Theory:
- [Neural Networks and Deep Learning](http://neuralnetworksanddeeplearning.com/)
- [Deep Learning Book - Chapter 6](https://www.deeplearningbook.org/contents/mlp.html)
- [CS231n Lecture Notes](http://cs231n.github.io/neural-networks-1/)

### Practical:
- [3Blue1Brown Neural Networks Series](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
- [Andrej Karpathy's micrograd](https://github.com/karpathy/micrograd)
- [Neural Networks from Scratch](https://nnfs.io/)

## 🧪 Experiments to Try

1. **Architecture Exploration**
   - Different number of hidden layers
   - Various hidden layer sizes
   - Impact of network depth vs width

2. **Activation Function Comparison**
   - Performance across different activations
   - Gradient flow analysis
   - Computational efficiency

3. **Learning Rate Optimization**
   - Fixed vs adaptive learning rates
   - Learning rate scheduling
   - Momentum and other optimizers

4. **Regularization Techniques**
   - L1 and L2 regularization
   - Dropout implementation
   - Early stopping strategies

## 🏆 Success Criteria

By the end of this session, you should be able to:
- ✅ Implement a neural network from scratch using only NumPy
- ✅ Explain the mathematics behind forward and backward propagation
- ✅ Train networks on real datasets and achieve reasonable performance
- ✅ Debug common training issues and apply appropriate solutions
- ✅ Understand the theoretical foundations of deep learning

## 🚧 Future Sessions Preview

- **Session 5**: Convolutional Neural Networks (CNNs)
- **Session 6**: Regularization and Optimization
- **Session 7**: Advanced Architectures (ResNets, DenseNets)
- **Session 8**: Transfer Learning and Fine-tuning

## 📝 Notes

This session forms the foundation for all subsequent deep learning topics. Take time to:
- Understand each mathematical concept thoroughly
- Implement everything from scratch before using frameworks
- Experiment with different parameters and observe their effects
- Document your learnings and insights

---

**Remember**: The goal is not just to make things work, but to understand *why* they work. Build strong fundamentals here! 🎯

## 📞 Support

If you encounter issues or have questions:
- Review the mathematical derivations step by step
- Check your implementations against known working examples
- Experiment with simpler problems first
- Don't hesitate to ask for help in course forums

---

*Happy Learning! Let's build some neural networks! 🧠✨*
