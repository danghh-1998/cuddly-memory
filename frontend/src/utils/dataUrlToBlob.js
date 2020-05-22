export default {
    dataURItoBlob: (dataURI) => {
        let byteString = atob(dataURI.split(',')[1]);
        let arrayBuffer = new ArrayBuffer(byteString.length);
        let intArray = new Uint8Array(arrayBuffer);
        for (let i = 0; i < byteString.length; i++) {
            intArray[i] = byteString.charCodeAt(i);
        }
        return new Blob([arrayBuffer], {type: 'image/png'});

    }
}