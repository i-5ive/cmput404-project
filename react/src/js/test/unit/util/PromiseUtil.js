export const
    /**
     * Creates an object that can be used to mock a Promise resolving instantly
     * @param {*} thenData - the argument passed to the then() that handles a promise being resolved
     * @param {*} errData - the argument passed to the catch() that handles a promise being rejected
     * @return {Object} - an object used to mock a Promise resolving instantly
     */
    createMockPromise = (thenData, errData) => {
        return {
            then: (callback) => {
                callback(thenData)
                return {
                    catch: (errCallback) => {
                        errCallback(errData);
                    }
                };
            }
        };
    };