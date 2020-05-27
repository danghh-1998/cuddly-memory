import {api} from "@/api";
import {imageApi} from "@/api"
import FormData from "form-data"

export default {
    uploadTemplate: (context, payload) => {
        return new Promise((resolve, reject) => {
            let reader = new FileReader()
            let file = payload.file.slice()
            reader.readAsDataURL(file)
            let result = null
            reader.onload = () => {
                result = reader.result
                context.commit('uploadTemplate', {
                    data: result,
                    templateName: payload.templateName
                })
                resolve(result)
            }
            reader.onerror = (e) => {
                reject(e)
            }
        })
    },
    createTemplate: (context, payload) => {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        let formData = new FormData()
        formData.append('name', payload.name)
        formData.append('folder_id', payload.folder_id)
        payload.bounding_boxes.reverse()
        formData.append('bounding_boxes', JSON.stringify(payload.bounding_boxes))
        let file = new File([payload.image], 'dummy.png', {type: 'image/png', lastModified: Date.now()})
        formData.append('image', file)
        return api.post(`templates/create`, formData)
            .then(() => {
            })
    },
    updateTemplate: function (context, payload) {
        api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
        let formData = new FormData()
        formData.append('bounding_boxes', JSON.stringify(payload.bounding_boxes))
        return api.put(`templates/${payload.templateId}/update`, formData)
            .then(() => {
            })
    },
    fetchTemplate: (context, payload) => {
        return new Promise((resolve, reject) => {
            let reader = new FileReader()
            let result = null
            let boundingBoxes = []
            api.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
            imageApi.get(`templates/${payload}/image/1?token=${localStorage.getItem('token')}`)
                .then((imageResponse) => {
                    let blob = new Blob([imageResponse.data], {type: 'image/png'})
                    api.get(`templates/${payload}`)
                        .then((response) => {
                            response.data.template.boundingBoxes.forEach((boundingBox) => {
                                let metadatas = JSON.parse(boundingBox.metadata)
                                let cornerLeft = metadatas[0]
                                let cornerRight = metadatas[1]
                                boundingBoxes.unshift({
                                    data: JSON.stringify({
                                        x: cornerLeft.x,
                                        y: cornerLeft.y,
                                        width: cornerRight.x - cornerLeft.x,
                                        height: cornerRight.y - cornerLeft.y,
                                        rotate: 0,
                                        scaleX: 1,
                                        scaleY: 1
                                    }),
                                    type: boundingBox.recognizeType,
                                    id: boundingBoxes.length,
                                    image: ''
                                })
                            })
                            reader.readAsDataURL(blob)
                            reader.onload = () => {
                                result = reader.result
                                context.commit('fetchTemplate', {
                                    image: result,
                                    template: {
                                        id: response.data.template.id,
                                        folder: response.data.template.folder,
                                        name: response.data.template.displayName,
                                        boundingBoxes: boundingBoxes
                                    }
                                })
                                resolve(result)
                            }
                            reader.onerror = (e) => {
                                reject(e)
                            }
                        })
                })
        })
    }
}
