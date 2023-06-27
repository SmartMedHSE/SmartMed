'use strict';

export let selectUnselectCheckbox = (ths, idx, field = '') => {
        idx = idx.toString()

        let settingsField = ths.settings[field]

        if (idx in settingsField) {
            if (settingsField[idx]) {
                ths.settings[field][idx] = false;
            } else {
                ths.settings[field][idx] = true;
            }
        } else {
            ths.settings[field][idx] = true;
        }
    };
