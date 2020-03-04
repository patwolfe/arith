import TealBlob from 'jumbosmash/assets/images/blob_teal.svg';
import BlueBlob from 'jumbosmash/assets/images/blob_blue.svg';

const top_left_foreground_cold = {
  style: {
    position: 'absolute', 
    left: -10, 
    top: -10,
    size: '100%'
  },
  height: 50,
  width: 50,
  zIndex: 2,
  image: TealBlob,
};
const top_left_background_cold = {
  style: {
    position: 'absolute',
    left: -20,
    top: -20,
    size: '100%',
  },
  height: 75,
  width: 75,
  zIndex: 1,
  image: BlueBlob,
};
const top_right_foreground_cold = {
  style: {
    position: 'absolute', 
    right: -10, 
    top: -10,
    size: '100%'
  },
  height: 50,
  width: 50,
  zIndex: 2,
  image: TealBlob,
};
const top_right_background_cold = {
  style: {
    position: 'absolute',
    right: -20,
    top: -20,
    size: '100%',
  },
  height: 75,
  width: 75,
  zIndex: 1,
  image: BlueBlob,
};
const bot_left_foreground_cold = {
  style: {
    position: 'absolute', 
    left: -10, 
    bottom: -10,
    size: '100%'
  },
  height: 50,
  width: 50,
  zIndex: 2,
  image: TealBlob,
};
const bot_left_background_cold = {
  style: {
    position: 'absolute',
    left: -20,
    bottom: -20,
    size: '100%',
  },
  height: 75,
  width: 75,
  zIndex: 1,
  image: BlueBlob,
};
const bot_right_foreground_cold = {
  style: {
    position: 'absolute', 
    right: -10, 
    bottom: -10,
    size: '100%'
  },
  height: 50,
  width: 50,
  zIndex: 2,
  image: TealBlob,
};
const bot_right_background_cold = {
  style: {
    position: 'absolute',
    right: -20,
    bottom: -20,
    size: '100%',
  },
  height: 75,
  width: 75,
  zIndex: 1,
  image: BlueBlob,
};

export default {
  cold_blobs: [top_left_background_cold, top_left_foreground_cold, top_right_background_cold, top_right_foreground_cold, bot_left_background_cold, bot_left_foreground_cold, bot_right_background_cold, bot_right_foreground_cold],
};