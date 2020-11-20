import os
import json
import cv2
import numpy as np

data_dir = '/home/tpatten/Data/bop/ycbv/test'
mask_dir = 'mask_visib'

# For each scene in the data directory
for scene_id in sorted(os.listdir(data_dir)):
    # Load scene_gt.json
    json_filename = os.path.join(data_dir, scene_id, 'scene_gt.json')
    with open(json_filename) as json_file:
        scene_gt = json.load(json_file)

    # Get all frame names
    for frame_id in sorted(os.listdir(os.path.join(data_dir, scene_id, 'rgb'))):
        print(scene_id, frame_id)
        # Get the key for this frame
        frame_key = str(int(frame_id.split('.')[0]))
        # Get the object ids
        object_ids = []
        for item in scene_gt[frame_key]:
            object_ids.append(item['obj_id'])

        # Load the masks for each
        mask = np.zeros((480, 640))
        mask = mask.flatten()
        for i in range(len(object_ids)):
            mask_filename = os.path.join(data_dir, scene_id, mask_dir,
                                         frame_id.split('.')[0] + '_' + str(i).zfill(6) + '.png')
            object_mask = cv2.imread(mask_filename)[:, :, 0]
            # For every index in object_mask that is 255, set to the object index in mask
            valid_idx = np.where(object_mask.flatten() == 255)[0]
            for v in valid_idx:
                mask[v] = object_ids[i]

        mask = mask.reshape((480, 640))

        # Visualize
        #img_output = np.hstack((mask, mask.astype(np.uint8)))
        #cv2.imshow('mask', img_output)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        # Save to file
        save_filename = os.path.join(data_dir, scene_id, mask_dir, frame_id)
        cv2.imwrite(save_filename, mask)
