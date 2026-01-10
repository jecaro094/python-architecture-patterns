from model.domain import Batch

def transform_batch(batch: Batch) -> Batch:
    """
    Transforms batch structure to be retrieved from swagger
    
    :param batch: Description
    :type batch: Batch
    :return: Description
    :rtype: Batch
    """
    transformed_batch = Batch(
        sku=batch.sku,
        quantity=batch.quantity,
        eta=batch.eta,
        orders=batch.orders,
    )
    transformed_batch.set_reference(batch.reference)
    return transformed_batch