# pendulum_NN
- Evolving neural nets controllers for the inversion and balancing of a pendulum.
- PyGame, NumPy, Keras (TF backend)

Two of many unique strategies found:

![](https://i.gyazo.com/fb60fa265c96b1dfeccb1d16e304f85a.gif) ![](https://i.gyazo.com/29696354e74c8048c366f08f7b300834.gif)

# Usage

For user play:
```
python main.py
```

For nn play:
- defaults to 'demo/161833.npy'
```
python main.py --purpose='nn' --weights={weights.npy}
```

For nn training
```
python main.py --purpose='train' --pop_size={int} --ngen={int} --lr={float} --elite_size={float} --seed_arr={weights.npy}
```

# Evolutionary algorithms: gradient-free network optimizers
- Alternative for traditional backpropagation-based parameter update schemes
- Massively parallelizable for large populations
- Capable of handling high dimensional parameter spaces

A population finds local maxima:

![](https://blog.otoro.net/assets/20171031/rastrigin/simplees.gif)

# Navigation

main.py
- Reads CLI arguments
- Executes simulation

game.py
- Loads pygame GUI
- Defines simulation parameters and simulation physics
- Computes simulation updates
- Interfaces with player/NN

pop.py
- Standalone genetic algorith module
- Modifies populations' parameters for gradient-free NN optimization!
- (See "Resources" below for phenomenal in-depth technical guides)

model.py
- Wraps [Keras's sequential class](https://keras.io/api/models/sequential/), defining model architecture and inference methods

display.py
- Customizable PyGame multi-slider menu to experiment during simulation

## Resources
[Visualizing Evolutionary Strategies, David Ha](https://blog.otoro.net/2017/10/29/visual-evolution-strategies/) 
 
[Evolutionary Strategies vs RL, Andrej Karpathy et al](https://openai.com/blog/evolution-strategies/)
