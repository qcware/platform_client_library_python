import qcware
import aiohttp
import asyncio
import random

Q = {(0, 0): 1, (0, 1): 1, (1, 1): 1, (1, 2): 1, (2, 2): -1}
P = {(0, 0): 1, (0, 1): 1, (1, 1): -1, (1, 2): 1, (2, 2): -1, (0, 3): 1, (1, 3): -1, (3, 2): 1}
solver = 'dwave_software'

async def get_solve_binary_result(client, M):
    rand_wait = random.randint(1, 5)
    await asyncio.sleep(rand_wait)
    print(rand_wait, M)
    result = await qcware.optimization.async_solve_binary(client, 'J582LKAst5zq', M, solver=solver)
    if 'solution' in result:
        print('Solution: ' + str(result['solution']))
    else:
        print('Error: ' + result['error'])

async def main():
    async with aiohttp.ClientSession() as client:
        tasks = [
            asyncio.ensure_future(get_solve_binary_result(client, Q)),
            asyncio.ensure_future(get_solve_binary_result(client, P)),
        ]

        await asyncio.wait(tasks)

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(main())
loop.run_until_complete(future)
