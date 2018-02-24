import numpy as np
import pandas as pd

from src.screening_algorithms.helpers.utils import Generator
from src.screening_algorithms.helpers.utils import Workers
from src.screening_algorithms.machine_ensemble import MachineEnsemble
from src.screening_algorithms.s_run import SRun

'''
z - proportion of cheaters
lr - loss ration, i.e., how much a False Negative is more harmful than a False Positive
votes_per_item - crowd votes per item for base round
worker_tests - number of test questions per worker
machine_tests - number of test items per machine classifier
corr - correlation of errors between machine classifiers
expert_cost - cost of an expert to label a paper (i.e., labels on all filters)
select_conf - confidence level that a machine has accuracy > 0.5
theta - overall proportion of positive items
filters_num - number of filters
filters_select - selectivity of filters (probability of applying a filter)
filters_dif - difficulty of filters
iter_num - number of iterations for averaging results
'''


if __name__ == '__main__':
    z = 0.3
    items_num = 500
    items_per_worker = 10
    baseround_items = 20  # must be a multiple of items_per_worker
    if baseround_items % items_per_worker:
        raise ValueError('baseround_items must be a multiple of items_per_worker')
    select_conf = 0.95
    worker_tests = 5
    votes_per_item = 3
    machine_tests = 50
    lr = 10
    expert_cost = 20
    filters_num = 2
    theta = 0.3
    filters_select = [0.14, 0.8]
    filters_dif = [0.9, 1.]
    iter_num = 50
    corr = 0.
    data = []

    params = {
        'filters_num': filters_num,
        'items_num': items_num,
        'baseround_items': baseround_items,
        'items_per_worker': items_per_worker,
        'votes_per_item': votes_per_item,
        'filters_select': filters_select,
        'filters_dif': filters_dif,
        'worker_tests': worker_tests,
        'lr': lr,
        'expert_cost': expert_cost,
        'corr': corr,
        'machine_tests': machine_tests,
        'select_conf': select_conf,
        'workers_accuracy': Workers(worker_tests, z).simulate_workers()
    }

    ground_truth = [0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    prior_prob_pos = [0.9848847073340017, 0.9963316950148308, 0.00017614937466972, 0.0011635924840544736, 0.9951674940004602, 0.004832505999539762, 0.9963316950148308, 0.9998238506253303, 0.36673773987206826, 0.004832505999539762, 0.9994434927784493, 0.11804347944841291, 0.9998238506253303, 0.00017614937466972, 0.9998238506253303, 0.9998238506253303, 0.9933957917370603, 0.004832505999539762, 0.9998238506253303, 0.7929312331924702, 0.9410451094238499, 0.4521575001310755, 0.00017614937466972, 0.5478424998689246, 0.9848847073340017, 0.0005565072215507426, 0.9998238506253303, 0.0005565072215507426, 0.9906143344709898, 0.0036683049851691596, 0.9994434927784493, 0.00017614937466972, 0.9998238506253303, 0.009385665529010247, 0.9848847073340017, 0.006604208262939644, 0.9998238506253303, 0.015115292665998306, 0.020578932019232943, 0.9951674940004602, 0.029073789194379376, 0.15486194477791115, 0.9998238506253303, 0.9998238506253303, 0.9906143344709898, 0.00017614937466972, 0.0005565072215507426, 0.0011635924840544736, 0.9988364075159456, 0.7929312331924702, 0.36673773987206826, 0.00017614937466972, 0.9988364075159456, 0.9848847073340017, 0.00017614937466972, 0.015115292665998308, 0.9994434927784493, 0.004832505999539762, 0.9578920644131728, 0.6332622601279317, 0.881956520551587, 0.7929312331924702, 0.9848847073340017, 0.0005565072215507426, 0.9848847073340017, 0.6332622601279317, 0.9998238506253303, 0.03110997311483804, 0.9688900268851619, 0.004832505999539762, 0.9709262108056207, 0.0036683049851691596, 0.9578920644131728, 0.9794210679807671, 0.8347248103531758, 0.004832505999539762, 0.9848847073340017, 0.004832505999539762, 0.9578920644131728, 0.015115292665998308, 0.9951674940004602, 0.0036683049851691596, 0.9988364075159456, 0.09213051823416507, 0.8451380552220888, 0.5305036998742615, 0.9998238506253303, 0.020578932019232943, 0.042107935586827225, 0.7027361644174819, 0.9933957917370603, 0.36673773987206826, 0.9988364075159456, 0.0005565072215507426, 0.5305036998742615, 0.09213051823416507, 0.881956520551587, 0.0036683049851691596, 0.9933957917370603, 0.015115292665998308, 0.9994434927784493, 0.020578932019232943, 0.9998238506253303, 0.9709262108056207, 0.9998238506253303, 0.09213051823416507, 0.006604208262939644, 0.004832505999539762, 0.9998238506253303, 0.5305036998742615, 0.9963316950148308, 0.00017614937466972, 0.00017614937466972, 0.0005565072215507426, 0.9951674940004602, 0.020578932019232943, 0.9998238506253303, 0.029073789194379376, 0.9963316950148308, 0.03110997311483804, 0.7027361644174819, 0.0005565072215507426, 0.9951674940004602, 0.9578920644131728, 0.9994434927784493, 0.00017614937466972, 0.9998238506253303, 0.5478424998689245, 0.9963316950148308, 0.00017614937466972, 0.9994434927784493, 0.00017614937466972, 0.9988364075159456, 0.8780155361753526, 0.9998238506253303, 0.00017614937466972, 0.36673773987206826, 0.0005565072215507426, 0.7027361644174819, 0.015115292665998306, 0.9951674940004602, 0.09213051823416506, 0.9994434927784493, 0.0011635924840544736, 0.9998238506253303, 0.2070687668075298, 0.9951674940004602, 0.0011635924840544736, 0.9998238506253303, 0.004832505999539762, 0.9688900268851619, 0.7929312331924702, 0.9848847073340017, 0.004832505999539762, 0.9994434927784493, 0.004832505999539762, 0.015115292665998306, 0.15486194477791113, 0.0036683049851691596, 0.004832505999539762, 0.9994434927784493, 0.009385665529010247, 0.9951674940004602, 0.0036683049851691596, 0.9998238506253303, 0.029073789194379376, 0.9078694817658349, 0.15486194477791115, 0.12198446382464737, 0.00017614937466972, 0.0005565072215507426, 0.009385665529010247, 0.9688900268851619, 0.020578932019232943, 0.9994434927784493, 0.00017614937466972, 0.9988364075159456, 0.0011635924840544736, 0.9951674940004602, 0.0005565072215507426, 0.9848847073340017, 0.006604208262939644, 0.9998238506253303, 0.015115292665998306, 0.9906143344709898, 0.9951674940004602, 0.6332622601279317, 0.0036683049851691596, 0.8347248103531758, 0.05895489057615009, 0.9688900268851619, 0.029073789194379376, 0.9998238506253303, 0.0005565072215507426, 0.9998238506253303, 0.03110997311483804, 0.015115292665998308, 0.9988364075159456, 0.9963316950148308, 0.00017614937466972, 0.9709262108056207, 0.015115292665998306, 0.8347248103531758, 0.0005565072215507426, 0.6332622601279317, 0.0005565072215507426, 0.9078694817658349, 0.9988364075159456, 0.9963316950148308, 0.006604208262939644, 0.9578920644131728, 0.009385665529010247, 0.9988364075159456, 0.00017614937466972, 0.9963316950148308, 0.0011635924840544736, 0.9906143344709898, 0.00017614937466972, 0.9906143344709898, 0.7929312331924702, 0.9988364075159456, 0.2070687668075298, 0.00017614937466972, 0.00017614937466972, 0.8347248103531758, 0.015115292665998308, 0.9998238506253303, 0.042107935586827225, 0.8780155361753526, 0.15486194477791115, 0.9933957917370603, 0.7929312331924702, 0.9078694817658349, 0.00017614937466972, 0.9848847073340017, 0.0011635924840544736, 0.042107935586827225, 0.03110997311483804, 0.9988364075159456, 0.9848847073340017, 0.15486194477791115, 0.0005565072215507426, 0.9848847073340017, 0.004832505999539762, 0.00017614937466972, 0.00017614937466972, 0.00017614937466972, 0.6332622601279317, 0.00017614937466972, 0.00017614937466972, 0.9988364075159456, 0.0011635924840544736, 0.9688900268851619, 0.0036683049851691596, 0.00017614937466972, 0.8451380552220888, 0.029073789194379376, 0.004832505999539762, 0.9994434927784493, 0.009385665529010247, 0.7027361644174819, 0.0011635924840544736, 0.9688900268851619, 0.15486194477791113, 0.9998238506253303, 0.00017614937466972, 0.9994434927784493, 0.00017614937466972, 0.7027361644174819, 0.0005565072215507426, 0.9963316950148308, 0.004832505999539762, 0.9994434927784493, 0.9998238506253303, 0.9998238506253303, 0.9998238506253303, 0.2070687668075298, 0.0011635924840544736, 0.9709262108056207, 0.015115292665998308, 0.9998238506253303, 0.9848847073340017, 0.9963316950148308, 0.8451380552220888, 0.9998238506253303, 0.0011635924840544736, 0.9933957917370603, 0.2070687668075298, 0.9410451094238499, 0.9848847073340017, 0.006604208262939644, 0.00017614937466972, 0.8451380552220888, 0.9951674940004602, 0.9998238506253303, 0.9933957917370603, 0.9933957917370603, 0.9951674940004602, 0.9848847073340017, 0.006604208262939644, 0.9951674940004602, 0.00017614937466972, 0.00017614937466972, 0.015115292665998308, 0.9998238506253303, 0.020578932019232943, 0.00017614937466972, 0.03110997311483804, 0.2070687668075298, 0.029073789194379376, 0.9848847073340017, 0.2972638355825182, 0.0005565072215507426, 0.0011635924840544736, 0.9951674940004602, 0.12198446382464737, 0.9963316950148308, 0.9994434927784493, 0.9994434927784493, 0.9994434927784493, 0.9951674940004602, 0.9794210679807671, 0.03110997311483804, 0.0036683049851691596, 0.9994434927784493, 0.015115292665998308, 0.9963316950148308, 0.0011635924840544736, 0.9933957917370603, 0.015115292665998308, 0.9998238506253303, 0.015115292665998306, 0.9933957917370603, 0.0005565072215507426, 0.9848847073340017, 0.7366369710467704, 0.9951674940004602, 0.0011635924840544736, 0.004832505999539762, 0.9994434927784493, 0.9988364075159456, 0.2972638355825182, 0.9988364075159456, 0.05895489057615009, 0.9933957917370603, 0.00017614937466972, 0.00017614937466972, 0.03110997311483804, 0.9998238506253303, 0.0036683049851691596, 0.9951674940004602, 0.00017614937466972, 0.9709262108056207, 0.004832505999539762, 0.9848847073340017, 0.0011635924840544736, 0.9578920644131728, 0.0011635924840544736, 0.9951674940004602, 0.015115292665998306, 0.9906143344709898, 0.006604208262939644, 0.9078694817658349, 0.004832505999539762, 0.9951674940004602, 0.004832505999539762, 0.9988364075159456, 0.5478424998689245, 0.9963316950148308, 0.015115292665998308, 0.9951674940004602, 0.11804347944841291, 0.46949630012573856, 0.36673773987206826, 0.9998238506253303, 0.015115292665998308, 0.00017614937466972, 0.015115292665998308, 0.9994434927784493, 0.9848847073340017, 0.7929312331924702, 0.09213051823416507, 0.9709262108056207, 0.015115292665998308, 0.0036683049851691596, 0.9951674940004602, 0.9848847073340017, 0.004832505999539762, 0.9994434927784493, 0.0011635924840544736, 0.9951674940004602, 0.015115292665998308, 0.9951674940004602, 0.09213051823416506, 0.9994434927784493, 0.0011635924840544736, 0.9848847073340017, 0.015115292665998308, 0.9078694817658349, 0.00017614937466972, 0.9688900268851619, 0.006604208262939644, 0.9951674940004602, 0.9998238506253303, 0.015115292665998308, 0.00017614937466972, 0.9848847073340017, 0.00017614937466972, 0.0005565072215507426, 0.9951674940004602, 0.9951674940004602, 0.004832505999539762, 0.9906143344709898, 0.9998238506253303, 0.9998238506253303, 0.2070687668075298, 0.9794210679807671, 0.015115292665998306, 0.12198446382464737, 0.029073789194379376, 0.9994434927784493, 0.00017614937466972, 0.9998238506253303, 0.0036683049851691596, 0.16527518964682417, 0.0005565072215507426, 0.9688900268851619, 0.0011635924840544736, 0.9688900268851619, 0.00017614937466972, 0.9998238506253303, 0.0011635924840544736, 0.881956520551587, 0.11804347944841291, 0.7027361644174819, 0.00017614937466972, 0.9994434927784493, 0.9078694817658349, 0.4521575001310755, 0.009385665529010247, 0.8451380552220888, 0.00017614937466972, 0.9994434927784493, 0.03110997311483804, 0.9078694817658349, 0.09213051823416506, 0.9951674940004602, 0.9963316950148308, 0.9951674940004602, 0.9410451094238499, 0.00017614937466972, 0.00017614937466972, 0.042107935586827225, 0.004832505999539762, 0.00017614937466972, 0.0011635924840544736, 0.4521575001310755, 0.2972638355825182, 0.9994434927784493, 0.03110997311483804, 0.9994434927784493, 0.9994434927784493, 0.9078694817658349, 0.0005565072215507426, 0.6332622601279317, 0.00017614937466972, 0.9994434927784493, 0.00017614937466972, 0.9998238506253303, 0.004832505999539762, 0.0036683049851691596, 0.020578932019232943, 0.004832505999539762, 0.9848847073340017, 0.9688900268851619, 0.004832505999539762, 0.0036683049851691596, 0.0005565072215507426, 0.7929312331924702, 0.9794210679807671, 0.00017614937466972, 0.15486194477791113, 0.9951674940004602, 0.0005565072215507426, 0.9994434927784493, 0.015115292665998308, 0.9988364075159456, 0.009385665529010247, 0.9951674940004602, 0.042107935586827225, 0.36673773987206826, 0.4521575001310755, 0.9951674940004602, 0.9848847073340017, 0.004832505999539762, 0.00017614937466972, 0.9998238506253303, 0.00017614937466972, 0.9078694817658349, 0.006604208262939644, 0.9998238506253303, 0.9578920644131728, 0.042107935586827225, 0.015115292665998306, 0.9998238506253303, 0.0036683049851691596, 0.9998238506253303, 0.11804347944841291, 0.9906143344709898, 0.0011635924840544736, 0.8780155361753526, 0.4521575001310755, 0.9848847073340017, 0.0005565072215507426, 0.9951674940004602, 0.9951674940004602, 0.9688900268851619, 0.0011635924840544736, 0.9848847073340017, 0.004832505999539762, 0.9951674940004602, 0.0005565072215507426, 0.9951674940004602, 0.0036683049851691596, 0.9906143344709898, 0.0005565072215507426, 0.9951674940004602, 0.03110997311483804, 0.9410451094238499, 0.9994434927784493, 0.9933957917370603, 0.006604208262939644, 0.00017614937466972, 0.004832505999539762, 0.9998238506253303, 0.15486194477791113, 0.9998238506253303, 0.004832505999539762, 0.9994434927784493, 0.0005565072215507426, 0.9998238506253303, 0.0011635924840544736, 0.9933957917370603, 0.0011635924840544736, 0.9994434927784493, 0.00017614937466972, 0.15486194477791113, 0.9963316950148308, 0.9994434927784493, 0.0011635924840544736, 0.9998238506253303, 0.004832505999539762, 0.9848847073340017, 0.00017614937466972, 0.9994434927784493, 0.03110997311483804, 0.8451380552220888, 0.9994434927784493, 0.9998238506253303, 0.9951674940004602, 0.9906143344709898, 0.015115292665998308, 0.9988364075159456, 0.00017614937466972, 0.09213051823416507, 0.0005565072215507426, 0.9848847073340017, 0.020578932019232943, 0.8451380552220888, 0.00017614937466972, 0.9410451094238499, 0.15486194477791113, 0.9998238506253303, 0.0011635924840544736, 0.9998238506253303, 0.7929312331924702, 0.9951674940004602, 0.00017614937466972, 0.9848847073340017, 0.0011635924840544736, 0.9933957917370603, 0.0005565072215507426, 0.9998238506253303, 0.2972638355825182, 0.9848847073340017, 0.004832505999539762, 0.9848847073340017, 0.0005565072215507426, 0.9994434927784493, 0.020578932019232943, 0.9994434927784493, 0.09213051823416506, 0.9998238506253303, 0.029073789194379376, 0.0005565072215507426, 0.7929312331924702, 0.0036683049851691596, 0.00017614937466972, 0.9951674940004602, 0.004832505999539762, 0.9688900268851619, 0.9963316950148308, 0.9688900268851619, 0.7027361644174819, 0.7929312331924702, 0.0036683049851691596, 0.9410451094238499, 0.00017614937466972, 0.9951674940004602, 0.9951674940004602, 0.9994434927784493, 0.0036683049851691596, 0.9998238506253303, 0.0011635924840544736, 0.9994434927784493, 0.004832505999539762, 0.16527518964682417, 0.11804347944841291, 0.09213051823416507, 0.029073789194379376, 0.9951674940004602, 0.029073789194379376, 0.9078694817658349, 0.015115292665998306, 0.9998238506253303, 0.0005565072215507426, 0.9994434927784493, 0.0011635924840544736, 0.9998238506253303, 0.6332622601279317, 0.004832505999539762, 0.00017614937466972, 0.9951674940004602, 0.0011635924840544736, 0.9998238506253303, 0.0005565072215507426, 0.9998238506253303, 0.09213051823416506, 0.9848847073340017, 0.36673773987206826, 0.8451380552220888, 0.03110997311483804, 0.9578920644131728, 0.2070687668075298, 0.9848847073340017, 0.9988364075159456, 0.9578920644131728, 0.9951674940004602, 0.009385665529010247, 0.0036683049851691596, 0.9688900268851619, 0.4521575001310755, 0.00017614937466972, 0.00017614937466972, 0.9951674940004602, 0.00017614937466972, 0.9998238506253303, 0.0005565072215507426, 0.9951674940004602, 0.00017614937466972, 0.9998238506253303, 0.00017614937466972, 0.9963316950148308, 0.0005565072215507426, 0.9933957917370603, 0.9988364075159456, 0.9988364075159456, 0.006604208262939644, 0.9998238506253303, 0.0036683049851691596, 0.9963316950148308, 0.0011635924840544736, 0.9998238506253303, 0.5478424998689246, 0.5305036998742615, 0.042107935586827225, 0.9688900268851619, 0.00017614937466972, 0.2633630289532295, 0.0005565072215507426, 0.8347248103531758, 0.00017614937466972, 0.009385665529010247, 0.9794210679807671, 0.9688900268851619, 0.0005565072215507426, 0.9998238506253303, 0.09213051823416506, 0.9988364075159456, 0.020578932019232943, 0.9794210679807671, 0.9688900268851619, 0.9848847073340017, 0.9848847073340017, 0.9998238506253303, 0.2972638355825182, 0.9994434927784493, 0.9906143344709898, 0.00017614937466972, 0.0005565072215507426, 0.9998238506253303, 0.0011635924840544736, 0.9998238506253303, 0.9794210679807671, 0.9963316950148308, 0.015115292665998306, 0.9998238506253303, 0.0036683049851691596, 0.015115292665998308, 0.8451380552220888, 0.9998238506253303, 0.0011635924840544736, 0.9963316950148308, 0.09213051823416506, 0.9994434927784493, 0.00017614937466972, 0.9951674940004602, 0.9906143344709898, 0.9709262108056207, 0.09213051823416507, 0.9988364075159456, 0.0011635924840544736, 0.9998238506253303, 0.15486194477791115, 0.9994434927784493, 0.9794210679807671, 0.9951674940004602, 0.00017614937466972, 0.03110997311483804, 0.015115292665998308, 0.881956520551587, 0.004832505999539762, 0.9848847073340017, 0.0005565072215507426, 0.9078694817658349, 0.15486194477791115, 0.9994434927784493, 0.00017614937466972, 0.9998238506253303, 0.0011635924840544736, 0.9410451094238499, 0.0011635924840544736, 0.8451380552220888, 0.0005565072215507426, 0.9998238506253303, 0.0005565072215507426, 0.9951674940004602, 0.16527518964682417, 0.03110997311483804, 0.9998238506253303, 0.9933957917370603, 0.9906143344709898, 0.9688900268851619, 0.004832505999539762, 0.9933957917370603, 0.00017614937466972, 0.05895489057615009, 0.6332622601279317, 0.9998238506253303, 0.00017614937466972, 0.9998238506253303, 0.00017614937466972, 0.9988364075159456, 0.004832505999539762, 0.9688900268851619, 0.03110997311483804, 0.00017614937466972, 0.00017614937466972, 0.00017614937466972, 0.2633630289532295, 0.9688900268851619, 0.9848847073340017, 0.881956520551587, 0.9794210679807671, 0.9988364075159456, 0.15486194477791115, 0.9078694817658349, 0.00017614937466972, 0.2972638355825182, 0.015115292665998306, 0.9988364075159456, 0.9988364075159456, 0.9906143344709898, 0.00017614937466972, 0.9794210679807671, 0.05895489057615009, 0.9688900268851619, 0.020578932019232943, 0.9994434927784493, 0.00017614937466972, 0.9988364075159456, 0.36673773987206826, 0.9988364075159456, 0.015115292665998306, 0.9794210679807671, 0.00017614937466972, 0.9988364075159456, 0.00017614937466972, 0.9998238506253303, 0.36673773987206826, 0.9994434927784493, 0.2070687668075298, 0.9848847073340017, 0.0011635924840544736, 0.9951674940004602, 0.0005565072215507426, 0.9998238506253303, 0.9994434927784493, 0.0005565072215507426, 0.00017614937466972, 0.9994434927784493, 0.9998238506253303, 0.0036683049851691596, 0.4521575001310755, 0.9994434927784493, 0.004832505999539762, 0.009385665529010247, 0.020578932019232943, 0.9688900268851619, 0.020578932019232943, 0.9988364075159456, 0.0005565072215507426, 0.9951674940004602, 0.09213051823416506, 0.9988364075159456, 0.00017614937466972, 0.9998238506253303, 0.9848847073340017, 0.9848847073340017, 0.0005565072215507426, 0.9794210679807671, 0.0036683049851691596, 0.9951674940004602, 0.004832505999539762, 0.9988364075159456, 0.00017614937466972, 0.4521575001310755, 0.36673773987206826, 0.0005565072215507426, 0.015115292665998308, 0.9998238506253303, 0.9688900268851619, 0.9951674940004602, 0.006604208262939644, 0.9963316950148308, 0.9988364075159456, 0.9688900268851619, 0.004832505999539762, 0.9688900268851619, 0.0036683049851691596, 0.9994434927784493, 0.015115292665998306, 0.9951674940004602, 0.03110997311483804, 0.9578920644131728, 0.0005565072215507426, 0.9998238506253303, 0.11804347944841291, 0.7027361644174819, 0.9988364075159456, 0.2972638355825182, 0.00017614937466972, 0.9688900268851619, 0.9998238506253303, 0.9578920644131728, 0.004832505999539762, 0.9988364075159456, 0.0005565072215507426, 0.9933957917370603, 0.004832505999539762, 0.0005565072215507426, 0.009385665529010247, 0.9410451094238499, 0.0005565072215507426, 0.36673773987206826, 0.9951674940004602, 0.9988364075159456, 0.0011635924840544736, 0.9994434927784493, 0.03110997311483804, 0.9998238506253303, 0.8451380552220888, 0.004832505999539762, 0.05895489057615009, 0.9933957917370603, 0.00017614937466972, 0.9994434927784493, 0.00017614937466972, 0.9906143344709898, 0.9998238506253303, 0.15486194477791115, 0.09213051823416506, 0.9709262108056207, 0.2972638355825182, 0.5478424998689246, 0.9078694817658349, 0.12198446382464737, 0.00017614937466972, 0.9848847073340017, 0.00017614937466972, 0.00017614937466972, 0.0005565072215507426, 0.9963316950148308, 0.09213051823416507, 0.9994434927784493, 0.09213051823416506, 0.03110997311483804, 0.5478424998689246, 0.9998238506253303, 0.9994434927784493, 0.7929312331924702, 0.004832505999539762, 0.9933957917370603, 0.9688900268851619, 0.9951674940004602, 0.9688900268851619, 0.4521575001310755, 0.0005565072215507426, 0.9988364075159456, 0.15486194477791113, 0.9988364075159456, 0.00017614937466972, 0.9994434927784493, 0.03110997311483804, 0.9994434927784493, 0.006604208262939644, 0.9951674940004602, 0.9848847073340017, 0.9994434927784493, 0.00017614937466972, 0.9688900268851619, 0.15486194477791115, 0.2633630289532295, 0.00017614937466972, 0.09213051823416507, 0.9998238506253303, 0.9994434927784493, 0.00017614937466972, 0.9933957917370603, 0.0005565072215507426, 0.4521575001310755, 0.0011635924840544736, 0.9963316950148308, 0.9998238506253303, 0.9794210679807671, 0.015115292665998306, 0.9963316950148308, 0.0005565072215507426, 0.0036683049851691596, 0.5305036998742615, 0.9994434927784493, 0.0005565072215507426, 0.8451380552220888, 0.020578932019232943, 0.9963316950148308, 0.11804347944841291, 0.00017614937466972, 0.0036683049851691596, 0.9848847073340017, 0.015115292665998308, 0.00017614937466972, 0.9578920644131728, 0.9998238506253303, 0.0036683049851691596, 0.9951674940004602, 0.0005565072215507426, 0.004832505999539762, 0.009385665529010247, 0.9688900268851619, 0.0036683049851691596, 0.9709262108056207, 0.0011635924840544736, 0.015115292665998306, 0.015115292665998308, 0.36673773987206826, 0.0036683049851691596, 0.9951674940004602, 0.00017614937466972, 0.9078694817658349, 0.015115292665998308, 0.9951674940004602, 0.009385665529010247, 0.9951674940004602, 0.004832505999539762, 0.8780155361753526, 0.004832505999539762, 0.5478424998689245, 0.9994434927784493, 0.8347248103531758, 0.0036683049851691596, 0.9951674940004602, 0.004832505999539762, 0.9998238506253303, 0.05895489057615009, 0.9906143344709898, 0.12198446382464737, 0.9988364075159456, 0.03110997311483804, 0.9688900268851619, 0.0005565072215507426]
    params.update({'ground_truth': ground_truth})

    # S-run algorithm
    loss_smrun_list = []
    cost_smrun_list = []
    rec_sm, pre_sm, f_sm, f_sm = [], [], [], []
    loss_me_list = []
    rec_me, pre_me, f_me, f_me = [], [], [], []

    loss_h_list = []
    cost_h_list = []
    rec_h, pre_h, f_h, f_h = [], [], [], []

    for _ in range(iter_num):
        # s-run
        params.update({
            'stop_score': 30,
            'prior_prob_pos': None
        })

        loss_smrun, cost_smrun, rec_sm_, pre_sm_, f_beta_sm = SRun(params).run()
        loss_smrun_list.append(loss_smrun)
        cost_smrun_list.append(cost_smrun)
        rec_sm.append(rec_sm_)
        pre_sm.append(pre_sm_)
        f_sm.append(f_beta_sm)


        # s-run with machine prior
        params.update({
            'stop_score': 15,
            'prior_prob_pos': prior_prob_pos.copy()
        })

        loss_h, cost_h, rec_h_, pre_h_, f_beta_h = SRun(params).run()
        loss_h_list.append(loss_h)
        cost_h_list.append(cost_h)
        rec_h.append(rec_h_)
        pre_h.append(pre_h_)
        f_h.append(f_beta_h)

    data.append([worker_tests, worker_tests, lr, np.mean(loss_smrun_list), np.std(loss_smrun_list),
                 np.mean(cost_smrun_list), np.std(cost_smrun_list), 'Crowd-Ensemble', np.mean(rec_sm),
                 np.std(rec_sm), np.mean(pre_sm), np.std(pre_sm), np.mean(f_sm), np.std(f_sm),
                 0., 0., select_conf, baseround_items, items_num, expert_cost, theta, filters_num])

    data.append([worker_tests, worker_tests, lr, np.mean(loss_h_list), np.std(loss_h_list),
                 np.mean(cost_h_list), np.std(cost_h_list), 'Hybrid-Ensemble', np.mean(rec_h),
                 np.std(rec_h), np.mean(pre_h), np.std(pre_h), np.mean(f_h), np.std(f_h),
                 machine_tests, corr, select_conf, baseround_items, items_num, expert_cost,
                 theta, filters_num])

    print('SM-RUN    loss: {:1.3f}, loss_std: {:1.3f}, recall: {:1.2f}, rec_std: {:1.3f}, '
          'price: {:1.2f}, price_std: {:1.2f}, precision: {:1.3f}, f_b: {}'
          .format(np.mean(loss_smrun_list), np.std(loss_smrun_list), np.mean(rec_sm),
                  np.std(rec_sm), np.mean(cost_smrun_list), np.std(cost_smrun_list),
                  np.mean(pre_sm), np.mean(f_sm)))
    print('H-RUN     loss: {:1.3f}, loss_std: {:1.3f}, ' 'recall: {:1.2f}, rec_std: {:1.3f}, '
          'price: {:1.2f}, price_std: {:1.2f}, precision: {:1.3f}, f_b: {}'
          .format(np.mean(loss_h_list), np.std(loss_h_list), np.mean(rec_h), np.std(rec_h),
                  np.mean(cost_h_list), np.std(cost_h_list), np.mean(pre_h), np.mean(f_h)))
    print('---------------------')

    pd.DataFrame(data,
                 columns=['worker_tests', 'worker_tests', 'lr', 'loss_mean', 'loss_std', 'price_mean', 'price_std',
                          'algorithm', 'recall', 'recall_std', 'precision', 'precision_std',
                          'f_beta', 'f_beta_std', 'machine_tests', 'corr', 'select_conf', 'baseround_items',
                          'total_items', 'expert_cost', 'theta', 'filters_num']
                 ).to_csv('../data/output_data/figXXX____.csv', index=False)
