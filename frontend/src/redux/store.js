// src/app/store.js
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import { api } from './slices/apiSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    [api.reducerPath]: api.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(api.middleware),
});