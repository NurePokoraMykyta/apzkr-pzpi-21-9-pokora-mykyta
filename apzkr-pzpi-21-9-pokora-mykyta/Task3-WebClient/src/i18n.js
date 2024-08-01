import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import HttpBackend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';
import translationEN from './locales/en/translation.json';
import translationUA from './locales/ua/translation.json';

const resources = {
    en: {
        translation: translationEN
    },
    ua: {
        translation: translationUA
    }
};

i18n
    .use(HttpBackend)
    .use(LanguageDetector)
    .use(initReactI18next)
    .init({
        resources,
        fallbackLng: 'en',
        supportedLngs: ['ua', 'en'],
        debug: true,
        detection: {
            order: ['cookie', 'localStorage', 'navigator'],
            caches: ['cookie'],
        },
        interpolation: {
            escapeValue: false,
        },
    });

export default i18n;