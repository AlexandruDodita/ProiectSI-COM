import json
import base64

class MessageSplitter:
    def __init__(self, block_size=1024):
        # dimensiunea blocului in bytes
        self.block_size = block_size

    def split_message(self, message):
        # imparte mesajul in blocuri
        if isinstance(message, str):
            message = message.encode('utf-8')

        blocks = []
        total_blocks = (len(message) + self.block_size - 1) // self.block_size

        for i in range(0, len(message), self.block_size):
            block = message[i:i + self.block_size]
            blocks.append({
                'block_num': len(blocks),
                'total_blocks': total_blocks,
                'data': base64.b64encode(block).decode('utf-8')
            })

        return blocks

    def reassemble_message(self, blocks):
        # reconstruieste mesajul din blocuri
        blocks_sorted = sorted(blocks, key=lambda x: x['block_num'])

        message_parts = []
        for block in blocks_sorted:
            data = base64.b64decode(block['data'])
            message_parts.append(data)

        return b''.join(message_parts)

    def split_file(self, filepath):
        # citeste si imparte un fisier
        with open(filepath, 'rb') as f:
            content = f.read()

        return self.split_message(content)

    def reassemble_to_file(self, blocks, output_path):
        # reconstruieste si salveaza intr-un fisier
        message = self.reassemble_message(blocks)

        with open(output_path, 'wb') as f:
            f.write(message)
