import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

const baseUrl = process.env.REACT_APP_BASE_URL;

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({
    baseUrl,
    prepareHeaders: (headers, { getState, endpoint }) => {
      // Exclude login and signup from the Authorization header
      if (endpoint !== 'login' && endpoint !== 'signup') {
        const token = getState().auth.accessToken;
        if (token) {
          headers.set('Authorization', `Bearer ${token}`);
        }
      }
      return headers;
    },
  }),
  tagTypes: ['Book'],
  endpoints: (builder) => ({
    login: builder.mutation({
      query: (credentials) => ({
        url: '/login',
        method: 'POST',
        body: credentials,
      }),
    }),
    signup: builder.mutation({
      query: (userData) => ({
        url: '/signup',
        method: 'POST',
        body: userData,
      }),
    }),
    getBooks: builder.query({
      query: ({ page, limit }) => `/books?page=${page}&limit=${limit}`,
      providesTags: ['Book'],
    }),
    createBook: builder.mutation({
      query: (bookData) => ({
        url: '/books',
        method: 'POST',
        body: bookData,
      }),
    }),
    updateBook: builder.mutation({
      query: ({ id, ...bookData }) => ({
        url: `/books/${id}`,
        method: 'PUT',
        body: bookData,
      }),
      invalidatesTags: ['Book'],
    }),
    deleteBook: builder.mutation({
      query: (id) => ({
        url: `/books/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: ['Book'],
    }),
  }),
});

// Export hooks for use in components
export const {
  useLoginMutation,
  useSignupMutation,
  useGetBooksQuery,
  useCreateBookMutation,
  useUpdateBookMutation, // Export the new updateBook hook
  useDeleteBookMutation,
} = api;
