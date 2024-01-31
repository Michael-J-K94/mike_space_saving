
import math

params = [] # N_entry, RFM_th, Counter-bits
#params.append([19, 8, 5])
#params.append([22, 32, 7])
#params.append([24, 128, 9])
#params.append([38, 8, 6])
#params.append([46, 32, 8])
#params.append([50, 128, 10])
#params.append([78, 8, 6])
#params.append([93, 32, 8])
#params.append([107, 128, 10])
#params.append([157, 8, 6])
#params.append([194, 32, 8])
#params.append([254, 128, 10])
#params.append([320, 8, 6])
#params.append([422, 32, 8])
#params.append([981, 128, 10])
#params.append([698, 8, 6])
#params.append([1122, 32, 8])
#params.append([1024, 32, 8])
params.append([369, 16, 7])
params.append([522, 64, 9])
params.append([984, 128, 10])
params.append([177, 16, 7])
params.append([214, 64, 9])
params.append([254, 128, 10])
params.append([420, 256, 11])
params.append([87, 16, 7])
params.append([99, 64, 9])
params.append([107, 128, 10])
params.append([123, 256, 11])
params.append([53, 256, 11])
params.append([25, 256, 10])
params.append([415, 16, 7])
params.append([583, 64, 9])
params.append([1186, 128, 10])
params.append([187, 16, 7])
params.append([223, 64, 9])
params.append([264, 128, 10])
params.append([439, 256, 11])
params.append([89, 16, 7])
params.append([101, 64, 9])
params.append([108, 128, 10])
params.append([124, 256, 11])
params.append([53, 256, 11])
params.append([25, 256, 10])


for param in params:

  r_file = open('rfm_unit_bank.v', 'r') 
  lines = r_file.readlines() 

  w_file = open('rfm_unit_bank/rfm_unit_bank_{}_{}_{}.v'.format(int(param[0]), int(param[1]), int(param[2])), 'w') 
    
  for line in lines:
    if line == "module rfm_unit_bank\n":
      line = "module rfm_unit_bank_{}_{}_{}\n".format(int(param[0]), int(param[1]), int(param[2]))
    if line == "  parameter NUM_ENTRY = 1024,\n":
      line = "  parameter NUM_ENTRY = {},\n".format(int(param[0]))
    if line == "  parameter NUM_ENTRY_BITS = 10, // log2 (NUM_ENTRY)\n":
      line = "  parameter NUM_ENTRY_BITS = {}, // log2 (NUM_ENTRY)\n".format(math.ceil(math.log2(param[0])))
    if line == "  parameter RFM_TH = 649,\n":
      line = "  parameter RFM_TH = {},\n".format(int(param[1]))
    if line == "  parameter CNT_SIZE = 13\n":
      line = "  parameter CNT_SIZE = {}\n".format(int(param[2]))
    if line == "cnt_cam #(.WORD_SIZE(CNT_SIZE), .ROW_NUM((NUM_ENTRY>>2)), .ENTRY_WIDTH(NUM_ENTRY_BITS-2)) cnt_cam_0 (cnt_cam_data_in_0, cnt_cam_addr_in_0, cnt_cam_read_en_0, cnt_cam_write_en_0, cnt_cam_search_en_0, cnt_cam_reset, cnt_cam_data_out_0, cnt_cam_addr_out_0, cnt_cam_match_0, clk, rstn, max_en, next_max_cnt_0);\n":
      line = "cnt_cam_{} #(.WORD_SIZE(CNT_SIZE), .ROW_NUM((NUM_ENTRY>>2)), .ENTRY_WIDTH(NUM_ENTRY_BITS-2)) cnt_cam_0 (cnt_cam_data_in_0, cnt_cam_addr_in_0, cnt_cam_read_en_0, cnt_cam_write_en_0, cnt_cam_search_en_0, cnt_cam_reset, cnt_cam_data_out_0, cnt_cam_addr_out_0, cnt_cam_match_0, clk, rstn, max_en, next_max_cnt_0);\n".format(int(param[0]))
    if line == "cnt_cam #(.WORD_SIZE(CNT_SIZE), .ROW_NUM((NUM_ENTRY>>2)), .ENTRY_WIDTH(NUM_ENTRY_BITS-2)) cnt_cam_1 (cnt_cam_data_in_1, cnt_cam_addr_in_1, cnt_cam_read_en_1, cnt_cam_write_en_1, cnt_cam_search_en_1, cnt_cam_reset, cnt_cam_data_out_1, cnt_cam_addr_out_1, cnt_cam_match_1, clk, rstn, max_en, next_max_cnt_1);\n":
      line = "cnt_cam_{} #(.WORD_SIZE(CNT_SIZE), .ROW_NUM((NUM_ENTRY>>2)), .ENTRY_WIDTH(NUM_ENTRY_BITS-2)) cnt_cam_1 (cnt_cam_data_in_1, cnt_cam_addr_in_1, cnt_cam_read_en_1, cnt_cam_write_en_1, cnt_cam_search_en_1, cnt_cam_reset, cnt_cam_data_out_1, cnt_cam_addr_out_1, cnt_cam_match_1, clk, rstn, max_en, next_max_cnt_1);\n".format(int(param[0]))
    if line == "cnt_cam #(.WORD_SIZE(CNT_SIZE), .ROW_NUM((NUM_ENTRY>>2)), .ENTRY_WIDTH(NUM_ENTRY_BITS-2)) cnt_cam_2 (cnt_cam_data_in_2, cnt_cam_addr_in_2, cnt_cam_read_en_2, cnt_cam_write_en_2, cnt_cam_search_en_2, cnt_cam_reset, cnt_cam_data_out_2, cnt_cam_addr_out_2, cnt_cam_match_2, clk, rstn, max_en, next_max_cnt_2);\n":
      line = "cnt_cam_{} #(.WORD_SIZE(CNT_SIZE), .ROW_NUM((NUM_ENTRY>>2)), .ENTRY_WIDTH(NUM_ENTRY_BITS-2)) cnt_cam_2 (cnt_cam_data_in_2, cnt_cam_addr_in_2, cnt_cam_read_en_2, cnt_cam_write_en_2, cnt_cam_search_en_2, cnt_cam_reset, cnt_cam_data_out_2, cnt_cam_addr_out_2, cnt_cam_match_2, clk, rstn, max_en, next_max_cnt_2);\n".format(int(param[0]))
    if line == "cnt_cam #(.WORD_SIZE(CNT_SIZE), .ROW_NUM((NUM_ENTRY>>2)), .ENTRY_WIDTH(NUM_ENTRY_BITS-2)) cnt_cam_3 (cnt_cam_data_in_3, cnt_cam_addr_in_3, cnt_cam_read_en_3, cnt_cam_write_en_3, cnt_cam_search_en_3, cnt_cam_reset, cnt_cam_data_out_3, cnt_cam_addr_out_3, cnt_cam_match_3, clk, rstn, max_en, next_max_cnt_3);\n":
      line = "cnt_cam_{} #(.WORD_SIZE(CNT_SIZE), .ROW_NUM((NUM_ENTRY>>2)), .ENTRY_WIDTH(NUM_ENTRY_BITS-2)) cnt_cam_3 (cnt_cam_data_in_3, cnt_cam_addr_in_3, cnt_cam_read_en_3, cnt_cam_write_en_3, cnt_cam_search_en_3, cnt_cam_reset, cnt_cam_data_out_3, cnt_cam_addr_out_3, cnt_cam_match_3, clk, rstn, max_en, next_max_cnt_3);\n".format(int(param[0]))

    w_file.write(line)

  r_file.close()
  w_file.close()
