import neural_networks.models as models
import neural_networks.net_utils as utils
import torch

net = models.MLP("example_MLP_network", [2, 10, 1])

dataset = utils.CSVDataset("example_csv.csv", [0, 1], [2])
dataloader = utils.create_dataloader(dataset, 2)

print(dataset.data, dataloader)
for input, labels in dataloader:
    print("input: ", input)
    print("labels: ", labels)
    print("predicted:", net(input))

optimizer = torch.optim.SGD(net.parameters(), lr=1, momentum=0.9)

# using same dataloader on train and eval just for example
utils.train(net, dataloader, dataloader, optimizer, torch.nn.L1Loss(), 5, 2)

for input, labels in dataloader:
    print("input: ", input)
    print("labels: ", labels)
    print("predicted:", net(input))

# saving net
utils.pickle_net(net, ".", suffix="example_suffix")
