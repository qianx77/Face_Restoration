from basicsr.utils.registry import Registry

class Registry_add(Registry):
    def __init__(self, name):
        super(Registry_add, self).__init__(name)
# vqfr add
QUANTIZER_REGISTRY = Registry_add('quantizer')
DECFUSE_REGISTRY = Registry_add('decodefuse')