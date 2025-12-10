def convert_memory_file():
    try:
        with open("Memory.txt", "r") as f_in:
            with open("Memory_Hex.txt", "w") as f_out:
                for line in f_in:
                    line = line.strip()
                    if not line:  # 空行
                        f_out.write("\n")
                        continue

                    if ':' in line:
                        addr_bin, content_bin = line.split(':', 1)

                        # 转换地址
                        addr_hex = '0x' + format(int(addr_bin, 2), '016X')

                        # 转换内容（每8位一组）
                        content_hex = ' '.join(
                            format(int(content_bin[i:i + 8], 2), '02X')
                            for i in range(0, len(content_bin), 8)
                        )

                        f_out.write(f"{addr_hex}:{content_hex}\n")

    except FileNotFoundError:
        print("错误: 找不到 Memory.txt 文件")
    except Exception as e:
        print(f"错误: {e}")

