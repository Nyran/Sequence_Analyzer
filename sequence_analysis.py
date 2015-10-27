import csv, re, sys, colorsys, os

#empty dictionary

# 1st key: child_id
# 2nd key: task_id
# 3rd key: phase_id
# value: list of events

events_per_children_per_task_per_phase_dictionary = {}
correlation_maps_per_children_per_task_per_phase_per_pattern = {}

correlation_maps_with_varying_task_per_children_and_phase = {}
correlation_maps_with_varying_phases_per_children_and_task = {}
correlation_maps_with_varying_children_per_task_and_phase = {}

registered_child_ids = []
registered_task_ids = []
registered_phase_ids = []

used_pattern = {}

combined_children_key = "combined_children"

min_color = [0,120,0]
max_color = [0,0,255]

svg_header_string = ""
svg_footer_string = ""
svg_correlation_rect_part_1_string = ""
svg_correlation_rect_part_2_string = ""
svg_correlation_rect_part_3_string = ""
svg_correlation_rect_part_4_string = ""
svg_correlation_rect_part_5_string = ""

event_layer_header_string = ""
svg_event_rect_part_1_string = ""
svg_event_rect_part_2_string = ""
svg_event_rect_part_2_grey_string = ""
svg_event_rect_part_3_string = ""
svg_event_rect_part_4_string = ""

svg_event_row_label_part_0_1_string =     "<text xml:space=\"preserve\" style=\"font-size:180px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans\" x=\""
svg_event_label_part_0_1_string =     "<text xml:space=\"preserve\" style=\"font-size:40px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans\" x=\""
svg_event_label_part_0_1_grey_string =     "<text xml:space=\"preserve\" style=\"font-size:40px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#757575;fill-opacity:1;stroke:none;font-family:Sans\" x=\""
svg_event_label_part_0_2_string = "\" y=\""
svg_event_label_part_1_string = ""
svg_event_label_part_2_string = ""
svg_event_label_part_3_string = ""
svg_event_label_part_4_string = ""

svg_event_row_label_part_3_string = ""

svg_event_sequenz_string = ""

layer_finalization_string = "</g>"
def load_inkscape_file_data():
  global svg_header_string
  global svg_footer_string
  global svg_correlation_rect_part_1_string
  global svg_correlation_rect_part_2_string
  global svg_correlation_rect_part_3_string
  global svg_correlation_rect_part_4_string
  global svg_correlation_rect_part_5_string

  global svg_event_rect_part_1_string
  global svg_event_rect_part_2_string
  global svg_event_rect_part_2_grey_string
  global svg_event_rect_part_3_string
  global svg_event_rect_part_4_string
  
  global event_layer_header_string

  global svg_event_label_part_1_string
  global svg_event_label_part_2_string
  global svg_event_label_part_3_string
  global svg_event_label_part_4_string

  global svg_event_row_label_part_3_string

  global svg_event_sequenz_string

  with open("svg_fragments/svg_header") as svg_header_file:
    for current_line in svg_header_file:
      svg_header_string += current_line
  svg_header_file.close()

  with open("svg_fragments/svg_footer") as svg_footer_file:
    for current_line in svg_footer_file:
      svg_footer_string += current_line
  svg_footer_file.close()

  with open("svg_fragments/svg_event_layer_header") as svg_event_layer_header_file:
    for current_line in svg_event_layer_header_file:
      event_layer_header_string += current_line
  svg_event_layer_header_file.close()

  with open("svg_fragments/svg_correlation_rect_part_1") as svg_correlation_rect_part_1_file:
    for current_line in svg_correlation_rect_part_1_file:
      svg_correlation_rect_part_1_string += current_line
  svg_correlation_rect_part_1_file.close()

  with open("svg_fragments/svg_correlation_rect_part_2") as svg_correlation_rect_part_2_file:
    for current_line in svg_correlation_rect_part_2_file:
      svg_correlation_rect_part_2_string += current_line
  svg_correlation_rect_part_2_file.close()

  with open("svg_fragments/svg_correlation_rect_part_3") as svg_correlation_rect_part_3_file:
    for current_line in svg_correlation_rect_part_3_file:
      svg_correlation_rect_part_3_string += current_line
  svg_correlation_rect_part_3_file.close()

  with open("svg_fragments/svg_correlation_rect_part_4") as svg_correlation_rect_part_4_file:
    for current_line in svg_correlation_rect_part_4_file:
      svg_correlation_rect_part_4_string += current_line
  svg_correlation_rect_part_4_file.close()

  with open("svg_fragments/svg_correlation_rect_part_5") as svg_correlation_rect_part_5_file:
    for current_line in svg_correlation_rect_part_5_file:
      svg_correlation_rect_part_5_string += current_line
  svg_correlation_rect_part_5_file.close()

  with open("svg_fragments/svg_event_rect_part_1") as svg_event_rect_part_1_file:
    for current_line in svg_event_rect_part_1_file:
      svg_event_rect_part_1_string += current_line
  svg_event_rect_part_1_file.close()

  with open("svg_fragments/svg_event_rect_part_2") as svg_event_rect_part_2_file:
    for current_line in svg_event_rect_part_2_file:
      svg_event_rect_part_2_string += current_line
  svg_event_rect_part_2_file.close()

  with open("svg_fragments/svg_event_rect_part_2_grey") as svg_event_rect_part_2_grey_file:
    for current_line in svg_event_rect_part_2_grey_file:
      svg_event_rect_part_2_grey_string += current_line
  svg_event_rect_part_2_grey_file.close()


  with open("svg_fragments/svg_event_rect_part_3") as svg_event_rect_part_3_file:
    for current_line in svg_event_rect_part_3_file:
      svg_event_rect_part_3_string += current_line
  svg_event_rect_part_3_file.close()

  with open("svg_fragments/svg_event_rect_part_4") as svg_event_rect_part_4_file:
    for current_line in svg_event_rect_part_4_file:
      svg_event_rect_part_4_string += current_line
  svg_event_rect_part_4_file.close()

  with open("svg_fragments/svg_event_label_part_1") as svg_event_label_part_1_file:
    for current_line in svg_event_label_part_1_file:
      svg_event_label_part_1_string += current_line
  svg_event_label_part_1_file.close()

  with open("svg_fragments/svg_event_label_part_2") as svg_event_label_part_2_file:
    for current_line in svg_event_label_part_2_file:
      svg_event_label_part_2_string += current_line
  svg_event_label_part_2_file.close()

  with open("svg_fragments/svg_event_label_part_3") as svg_event_label_part_3_file:
    for current_line in svg_event_label_part_3_file:
      svg_event_label_part_3_string += current_line
  svg_event_label_part_3_file.close()

  with open("svg_fragments/svg_event_label_part_4") as svg_event_label_part_4_file:
    for current_line in svg_event_label_part_4_file:
      svg_event_label_part_4_string += current_line
  svg_event_label_part_4_file.close()

  with open("svg_fragments/svg_event_row_label_part_3") as svg_event_row_label_part_3_file:
    for current_line in svg_event_row_label_part_3_file:
      svg_event_row_label_part_3_string += current_line
  svg_event_row_label_part_3_file.close()

  with open("svg_fragments/svg_event_sequenz_string") as svg_event_sequenz_string_file:
    for current_line in svg_event_sequenz_string_file:
      svg_event_sequenz_string += current_line
  svg_event_sequenz_string_file.close()

def create_inkscape_file(base_path, encountered_string_list, encountered_event_list, encountered_correlations_list, pattern):
  full_path = base_path+"/output.svg"

  output_file = open(full_path, "w")

  output_file.write(svg_header_string)
  
  #print(pattern)
  pattern_components = pattern.split(",")
  #print(pattern_components)
  #print("len: " + str(len(encountered_event_list[0])) + "..." + str(len(encountered_correlations_list[0])) )

  width_per_corr_rect = 172.85715
  height_per_corr_rect = 81.428574
  initial_offset_corr_rect_x = 5.0000005
  initial_offset_corr_rect_y = -40.961945
  current_offset_corr_rect_x = initial_offset_corr_rect_x
  current_offset_corr_rect_y = initial_offset_corr_rect_y

  width_per_event_rect = 172.85715
  height_per_event_rect = 81.428574
  initial_offset_event_rect_x = 67.14286
  initial_offset_event_rect_y = 120.93361
  current_offset_event_rect_x = initial_offset_event_rect_x
  current_offset_event_rect_y = initial_offset_event_rect_y

  initial_offset_string_x = 130.2731
  initial_offset_string_y = 179.51898
  current_offset_string_x = initial_offset_string_x
  current_offset_string_y = initial_offset_string_y
  
  initial_offset_event_row_label_x = 50.2731
  initial_offset_event_row_label_y = 29.51898
  current_offset_event_row_label_x = initial_offset_event_row_label_x 
  current_offset_event_row_label_y = initial_offset_event_row_label_y 


  global svg_event_rect_part_1_string
  global svg_event_sequenz_string

  for correlation_rect_list in encountered_correlations_list:
    for correlation_rect_val in correlation_rect_list:
      greyscale_value = int (correlation_rect_val * 255)
      greyscale_value = min(255, max(0, greyscale_value) )
      greyscale_hex = ("%02x%02x%02x" % (greyscale_value, greyscale_value, greyscale_value))
      #print(greyscale_hex)
      output_file.write(svg_correlation_rect_part_1_string)
      output_file.write(greyscale_hex)
      output_file.write(svg_correlation_rect_part_2_string)
      output_file.write("000000")
      output_file.write(svg_correlation_rect_part_3_string)
      output_file.write(str(current_offset_corr_rect_x) )
      output_file.write(svg_correlation_rect_part_4_string)
      output_file.write( str(current_offset_corr_rect_y) )
      output_file.write(svg_correlation_rect_part_5_string)

      current_offset_corr_rect_x += width_per_corr_rect
  
    current_offset_corr_rect_y += 6*height_per_corr_rect
    current_offset_corr_rect_x = initial_offset_corr_rect_x
  current_offset_corr_rect_y = initial_offset_corr_rect_y
  output_file.write(layer_finalization_string)
  output_file.write(event_layer_header_string)
  


  for event_list in encountered_event_list:
    for encountered_event in event_list:
      svg_event_rect_part_1_string = svg_event_rect_part_1_string.strip()
      output_file.write(svg_event_rect_part_1_string)
      output_file.write("ffffff")
      output_file.write(svg_event_rect_part_2_string)
      output_file.write(str(current_offset_event_rect_x) )
      output_file.write(svg_event_rect_part_3_string)
      output_file.write(str(current_offset_event_rect_y) )
      output_file.write(svg_event_rect_part_4_string)

      output_file.write(svg_event_label_part_0_1_string)
      output_file.write(str(current_offset_string_x - len(encountered_event) * 15) ) 
      output_file.write(svg_event_label_part_0_2_string)
      output_file.write(str(current_offset_string_y) )
      output_file.write(svg_event_label_part_1_string)
      output_file.write(str(current_offset_string_x - len(encountered_event) * 15) )
      output_file.write(svg_event_label_part_2_string)
      output_file.write(str(current_offset_string_y) )
      output_file.write(svg_event_label_part_3_string)
      output_file.write(encountered_event)
      output_file.write(svg_event_label_part_4_string)

      current_offset_string_x += width_per_event_rect
      current_offset_event_rect_x += width_per_event_rect
    current_offset_event_rect_y += 6*height_per_event_rect
    current_offset_event_rect_x = initial_offset_event_rect_x
    current_offset_string_y += 6*height_per_event_rect
    current_offset_string_x = initial_offset_string_x
  current_offset_event_rect_y = initial_offset_event_rect_y
  current_offset_string_y = initial_offset_string_y

  for event_row_label in encountered_string_list:
    output_file.write(svg_event_row_label_part_0_1_string)
    output_file.write(str(current_offset_event_row_label_x - 20) ) 
    output_file.write(svg_event_label_part_0_2_string)
    output_file.write(str(current_offset_event_row_label_y) )
    output_file.write(svg_event_label_part_1_string)
    output_file.write(str(current_offset_event_row_label_x - 20 ))
    output_file.write(svg_event_label_part_2_string)
    output_file.write(str(current_offset_event_row_label_y) )
    output_file.write(svg_event_row_label_part_3_string)
    output_file.write(event_row_label)
    output_file.write(svg_event_label_part_4_string)

    current_offset_event_row_label_y += 6*height_per_event_rect


  output_file.write(svg_event_sequenz_string)

  initial_offset_string_x = 130.2731
  initial_offset_string_y = -149.51898
  current_offset_string_x = initial_offset_string_x
  current_offset_string_y = initial_offset_string_y

  width_per_event_rect = 172.85715
  height_per_event_rect = 81.428574
  initial_offset_event_rect_x = 67.14286
  initial_offset_event_rect_y = -208.93361
  current_offset_event_rect_x = initial_offset_event_rect_x
  current_offset_event_rect_y = initial_offset_event_rect_y

  for pattern_element in pattern_components:
    svg_event_rect_part_1_string = svg_event_rect_part_1_string.strip()
    output_file.write(svg_event_rect_part_1_string)
    output_file.write("ffffff")
    output_file.write(svg_event_rect_part_2_grey_string)
    output_file.write(str(current_offset_event_rect_x) )
    output_file.write(svg_event_rect_part_3_string)
    output_file.write(str(current_offset_event_rect_y) )
    output_file.write(svg_event_rect_part_4_string)

    output_file.write(svg_event_label_part_0_1_grey_string)
    output_file.write(str(current_offset_string_x - len(pattern_element) * 15) ) 
    output_file.write(svg_event_label_part_0_2_string)
    output_file.write(str(current_offset_string_y) )
    output_file.write(svg_event_label_part_1_string)
    output_file.write(str(current_offset_string_x - len(pattern_element) * 15) )
    output_file.write(svg_event_label_part_2_string)
    output_file.write(str(current_offset_string_y) )
    output_file.write(svg_event_label_part_3_string)
    output_file.write(pattern_element)
    output_file.write(svg_event_label_part_4_string)

    current_offset_string_x += width_per_event_rect
    current_offset_event_rect_x += width_per_event_rect

  output_file.write(layer_finalization_string)
  output_file.write(svg_footer_string)

  output_file.close()

def clear_used_patterns():
  used_pattern = {}


def compute_correlation_for(current_child_idx, inner_task_idx, current_phase_idx, current_pattern_list, current_pattern_string, map_to_use):
  current_event_sequence = events_per_children_per_task_per_phase_dictionary[current_child_idx][inner_task_idx][current_phase_idx]

  current_correlation_map_list = []

  N_gramm_length = len(current_pattern_list)
  current_sequence_length = len(current_event_sequence)
  # now go to the end of the sequence (if the sequence tail is smaller than the N-Gramm length, we consider the missing elements as
  # miss

  for pattern_extraction_offset in range(current_sequence_length):
    matches_in_a_row = 0
    for pattern_element_offset in range(N_gramm_length):
      if pattern_extraction_offset + pattern_element_offset < current_sequence_length:
        if current_pattern_list[pattern_element_offset] == current_event_sequence[pattern_extraction_offset + pattern_element_offset]:
          matches_in_a_row += 1
        else:
          # pattern did not match at this part, sequence can not be continued
          break
      else:
        #the event sequence is over
        break
    #print(matches_in_a_row/float(N_gramm_length))
    current_correlation_map_list.append(matches_in_a_row/float(N_gramm_length));
    #print("NGL: " + str(N_gramm_length) )

  map_to_use[current_child_idx][inner_task_idx][current_phase_idx][current_pattern_string]  = current_correlation_map_list
    

def check_and_insert_child_idx(child_idx):
  if child_idx not in events_per_children_per_task_per_phase_dictionary:
    #append new empty dictionary, which will contain events per phase per task
    events_per_children_per_task_per_phase_dictionary[child_idx] = {}
    correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx] = {}
    correlation_maps_with_varying_task_per_children_and_phase[child_idx] = {}
    correlation_maps_with_varying_phases_per_children_and_task[child_idx] = {}
    correlation_maps_with_varying_children_per_task_and_phase[child_idx] = {}

def check_and_insert_task_idx(child_idx, task_idx):
  if task_idx not in events_per_children_per_task_per_phase_dictionary[child_idx]:
    #append new empty dictionary, which will contain events per phase
    events_per_children_per_task_per_phase_dictionary[child_idx][task_idx] = {}
    correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx][task_idx] = {}
    correlation_maps_with_varying_task_per_children_and_phase[child_idx][task_idx] = {}
    correlation_maps_with_varying_phases_per_children_and_task[child_idx][task_idx] = {}
    correlation_maps_with_varying_children_per_task_and_phase[child_idx][task_idx] = {}

def check_and_insert_phase_idx(child_idx, task_idx, phase_idx):
  if phase_idx not in events_per_children_per_task_per_phase_dictionary[child_idx][task_idx]:
    #append empty event list
    events_per_children_per_task_per_phase_dictionary[child_idx][task_idx][phase_idx] = []

    #append empty dictionary, that will contain the correlation for every possible pattern (massive dictionary for large n-gramms)
    correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx][task_idx][phase_idx] = {}
    correlation_maps_with_varying_task_per_children_and_phase[child_idx][task_idx][phase_idx] = {}
    correlation_maps_with_varying_phases_per_children_and_task[child_idx][task_idx][phase_idx] = {}
    correlation_maps_with_varying_children_per_task_and_phase[child_idx][task_idx][phase_idx] = {}

def append_events(child_idx, task_idx, phase_idx, event_list):
  for event in event_list:
    events_per_children_per_task_per_phase_dictionary[child_idx][task_idx][phase_idx].append(event)

def insert_event_list_entry(child_idx, task_idx, phase_idx, event_list):
  check_and_insert_child_idx(child_idx)
  check_and_insert_task_idx(child_idx, task_idx)
  check_and_insert_phase_idx(child_idx, task_idx, phase_idx)

  #since we checked, that the data structure is complete, we insert the data
  append_events(child_idx, task_idx, phase_idx, event_list)
  

def load_cell_file(file_path):
  with open(file_path) as cell_file:
    for current_line in cell_file:
      #current_line = re.sub("-","",current_line)
      current_line = re.sub("\r\n","",current_line)
      splitted_array = current_line.split(";")
      #print(splitted_array)
      #print(len(splitted_array))
      
      splitted_array_length = len(splitted_array)

      current_child_idx = splitted_array[0]
      current_task_idx = splitted_array[1]
      current_phase_idx = splitted_array[2]

      if current_phase_idx == '1' or current_phase_idx == '2' or current_phase_idx == '3':
        current_phase_idx = "1 Pre-Aufgabe"
      elif current_phase_idx == '4':
        current_phase_idx = "2 Aufgabe"
      else:
        current_phase_idx = "3 Post-Aufgabe"

      if splitted_array_length > 3:
        current_event_list = splitted_array[3:]
      else:
        current_event_list = []

      list_index = 0
      for event in current_event_list:
        if event == "PT_T" or event == "PT_A":
          #print("FOUND OCURRENCE")
          current_event_list[list_index] = "PT"
        elif event == "S_L" or event == "S_V" or event == "S_S":
          current_event_list[list_index] = "S"

        list_index += 1

      insert_event_list_entry(current_child_idx, current_task_idx, current_phase_idx, current_event_list)
      #cell_id = result_list[1]
      #cell_id_length = len(cell_id)
      #if cell_id_length > 0:
        #child_id = result_list[0]
        #insert_cell_entry(child_id, cell_id)

  #print(events_per_children_per_task_per_phase_dictionary)


#def compare_same_taks_for_different_phases_of_individual_children():

def compare_same_phases_for_different_tasks_of_individual_children():
  for current_child_idx in events_per_children_per_task_per_phase_dictionary:
    for current_task_idx in events_per_children_per_task_per_phase_dictionary[current_child_idx]:
      for current_phase_idx in events_per_children_per_task_per_phase_dictionary[current_child_idx][current_task_idx]:
        #for inner_task_idx in events_per_children_per_task_per_phase_dictionary[current_child_idx]:
        if current_phase_idx in events_per_children_per_task_per_phase_dictionary[current_child_idx][current_task_idx]:
           #print(events_per_children_per_task_per_phase_dictionary[current_child_idx][current_task_idx])
            
           #actual analyzation
           current_event_sequence = events_per_children_per_task_per_phase_dictionary[current_child_idx][current_task_idx][current_phase_idx]
           current_sequence_length = len(current_event_sequence)

           current_pattern_string = ""
           current_pattern_list = []

           max_N_gramm_length = 20

           for N_gramm_length in range(2,max_N_gramm_length+1):

             for pattern_extraction_offset in range(current_sequence_length-(N_gramm_length-1)):
               current_pattern_string = ""
               current_pattern_list = []
               #print("Pattern: ")
               for pattern_iterator in range(N_gramm_length):
                 current_pattern_list.append(current_event_sequence[pattern_extraction_offset + pattern_iterator])
                 if len(current_pattern_string) != 0:
                   current_pattern_string += ","
                 current_pattern_string += current_event_sequence[pattern_extraction_offset + pattern_iterator]
               #print("Whole key string:")
               #print(current_pattern_string)

               #only use patterns we did not use during this analyzation
               if current_pattern_string not in used_pattern:
                 #insert the pattern now that we are going to use it to prevent us from reusing it again
                 used_pattern[current_pattern_string] = 1
                 for inner_child_iteration_idx in events_per_children_per_task_per_phase_dictionary:
                   if inner_child_iteration_idx not in registered_child_ids:
                     registered_child_ids.append(inner_child_iteration_idx)
                   for inner_task_iteration_idx in events_per_children_per_task_per_phase_dictionary[inner_child_iteration_idx]:
                      if inner_task_iteration_idx  not in registered_task_ids:
                        registered_task_ids.append(inner_task_iteration_idx)
                      for inner_phase_iteration_idx in events_per_children_per_task_per_phase_dictionary[inner_child_iteration_idx][inner_task_iteration_idx]:
                        compute_correlation_for(inner_child_iteration_idx, inner_task_iteration_idx, inner_phase_iteration_idx, current_pattern_list, current_pattern_string, correlation_maps_per_children_per_task_per_phase_per_pattern)
                        if inner_phase_iteration_idx not in registered_phase_ids:
                          registered_phase_ids.append(inner_phase_iteration_idx)


  registered_child_ids.sort()
  registered_task_ids.sort()
  registered_phase_ids.sort()
    
#replace this string for cour custom csv file
load_cell_file("VideoDaten_nebeneinander.csv")
clear_used_patterns()
compare_same_phases_for_different_tasks_of_individual_children()


total_num_correlations = 0
for child_entry in correlation_maps_per_children_per_task_per_phase_per_pattern:
  for task_entry in correlation_maps_per_children_per_task_per_phase_per_pattern[child_entry]:
    for phase_entry in correlation_maps_per_children_per_task_per_phase_per_pattern[child_entry][task_entry]:
      total_num_correlations += len(correlation_maps_per_children_per_task_per_phase_per_pattern[child_entry][task_entry][phase_entry])

used_pattern = list(set(used_pattern))

load_inkscape_file_data()


max_num_occurences = 10

#keep task and phase constant (evaluate between children)
for task_idx in registered_task_ids:
  for phase_idx in registered_phase_ids:
    #create folders here
    #evaluate patterns over the children
    for pattern in used_pattern:
      N_gramm_length = len(pattern.split(',') )
      num_correlations_over_fifty_percent = 0

      encountered_string_list = []
      encountered_event_list = []
      encountered_correlations_list = []

      for child_idx in registered_child_ids:
        if task_idx in correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx]:
          if phase_idx in correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx][task_idx]:
            correlation_list_for_pattern = correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx][task_idx][phase_idx][pattern]

            encountered_string_list.append("Kind " + child_idx)
            encountered_event_list.append( events_per_children_per_task_per_phase_dictionary[child_idx][task_idx][phase_idx] )
            encountered_correlations_list.append(correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx][task_idx][phase_idx][pattern])
            event_entry_counter = 0
            for correlation_entry in correlation_list_for_pattern:
              if correlation_entry > 0.99999:
                num_correlations_over_fifty_percent += 1

              event_entry_counter += 1
          else:
            encountered_string_list.append("Kind " + child_idx)
            encountered_event_list.append( [] )
            encountered_correlations_list.append( [] )
            event_entry_counter = 0
        else:
          encountered_string_list.append("Kind " + child_idx)
          encountered_event_list.append( [] )
          encountered_correlations_list.append( [] )
          event_entry_counter = 0
      for occurence_iterator in range(2,(max_num_occurences+1)):

        if num_correlations_over_fifty_percent == occurence_iterator:
          base_path = "./children_comparison_with_constant_phase_and_task/aufgabe_"+task_idx+"/"+phase_idx+"/"+str(N_gramm_length)+"_gramm/"+str(occurence_iterator)+"_occurences/pattern___"+pattern
          if not os.path.exists(base_path):
            #print("Creating directory: " + base_path)
            os.makedirs(base_path)
          create_inkscape_file(base_path, encountered_string_list, encountered_event_list, encountered_correlations_list, pattern)
      #print(pattern)


#keep child and phase constant (evaluate between children)
for child_idx in registered_child_ids:
  for phase_idx in registered_phase_ids:
    #create folders here
    #evaluate patterns over the children
    for pattern in used_pattern:
      N_gramm_length = len(pattern.split(',') )
      num_correlations_over_fifty_percent = 0

      encountered_string_list = []
      encountered_event_list = []
      encountered_correlations_list = []

      for task_idx in registered_task_ids:

        if task_idx in correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx]:
          if phase_idx in correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx][task_idx]:
            correlation_list_for_pattern = correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx][task_idx][phase_idx][pattern]

            encountered_string_list.append("Aufgabe " + task_idx)
            encountered_event_list.append( events_per_children_per_task_per_phase_dictionary[child_idx][task_idx][phase_idx] )
            encountered_correlations_list.append(correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx][task_idx][phase_idx][pattern])
            event_entry_counter = 0
            for correlation_entry in correlation_list_for_pattern:
              if correlation_entry > 0.99999:
                num_correlations_over_fifty_percent += 1
              event_entry_counter += 1
          else:
            encountered_string_list.append("Aufgabe " + task_idx)
            encountered_event_list.append( [] )
            encountered_correlations_list.append( [] )
            event_entry_counter = 0
        else:
          encountered_string_list.append("Aufgabe " + task_idx)
          encountered_event_list.append( [] )
          encountered_correlations_list.append( [] )
          event_entry_counter = 0
      for occurence_iterator in range(2,(max_num_occurences+1)):

        if num_correlations_over_fifty_percent == occurence_iterator:
          base_path = "./task_comparison_with_constant_phase_and_child/kind_"+child_idx+"/"+phase_idx+"/"+str(N_gramm_length)+"_gramm/"+str(occurence_iterator)+"_occurences/pattern___"+pattern
          if not os.path.exists(base_path):
            #print("Creating directory: " + base_path)
            os.makedirs(base_path)
          create_inkscape_file(base_path, encountered_string_list, encountered_event_list, encountered_correlations_list, pattern)
      #print(pattern)


#keep child and task constant (evaluate between children)
for child_idx in registered_child_ids:
  for task_idx in registered_task_ids:
    #create folders here
    #evaluate patterns over the children
    for pattern in used_pattern:
      N_gramm_length = len(pattern.split(',') )
      num_correlations_over_fifty_percent = 0

      encountered_string_list = []
      encountered_event_list = []
      encountered_correlations_list = []

      for phase_idx in registered_phase_ids:
        if task_idx in correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx]:
          if phase_idx in correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx][task_idx]:
            correlation_list_for_pattern = correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx][task_idx][phase_idx][pattern]

            encountered_string_list.append(phase_idx)
            encountered_event_list.append( events_per_children_per_task_per_phase_dictionary[child_idx][task_idx][phase_idx] )
            encountered_correlations_list.append(correlation_maps_per_children_per_task_per_phase_per_pattern[child_idx][task_idx][phase_idx][pattern])
            event_entry_counter = 0

            for correlation_entry in correlation_list_for_pattern:
              if correlation_entry > 0.99999:
                num_correlations_over_fifty_percent += 1
          else:
            encountered_string_list.append(phase_idx)
            encountered_event_list.append( [] )
            encountered_correlations_list.append( [] )
            event_entry_counter = 0
        else:
          encountered_string_list.append(phase_idx)
          encountered_event_list.append( [] )
          encountered_correlations_list.append( [] )
          event_entry_counter = 0
      for occurence_iterator in range(2,(max_num_occurences+1)):

        if num_correlations_over_fifty_percent == occurence_iterator:
          base_path = "./phase_comparison_with_constant_task_and_child/Aufgabe_"+task_idx+"/Kind_"+child_idx+"/"+str(N_gramm_length)+"_gramm/"+str(occurence_iterator)+"_occurences/pattern___"+pattern
          if not os.path.exists(base_path):
            #print("Creating directory: " + base_path)
            os.makedirs(base_path)
          create_inkscape_file(base_path, encountered_string_list, encountered_event_list, encountered_correlations_list, pattern)
      #print(pattern)


        
