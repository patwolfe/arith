import * as Permissions from 'expo-permissions';

async function getPermissionAsync(alertMessage) {
  const { status } = await Permissions.askAsync(Permissions.CAMERA_ROLL);
  if (status !== 'granted') {
    alert(alertMessage);
  }
  return status;
}

async function getCameraPermissionAsync(alertMessage) {
  const { status } = await Permissions.askAsync(Permissions.CAMERA);
  if (status !== 'granted') {
    alert(alertMessage);
  }
  return status;
}

export { getPermissionAsync, getCameraPermissionAsync};