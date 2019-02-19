import { ClientFunction } from 'testcafe';

export const
    // Credit to Alexander Moskovkin from https://stackoverflow.com/a/44880118     
    getURL = ClientFunction(() => window.location.href),

    /**
     * Gets whether the user is currently logged in or not
     * @param {Object} t - the testcafe runner
     * @return {boolean} - whether the user is currently logged in or not
     */
    isLoggedIn = async (t) => {
        return t.eval(() => {
            return DEV_AUTH_STORE.state.isLoggedIn;
        });
    };