import React, { useState, useEffect } from 'react';
import { Table, Pagination, Button, Space, Popconfirm, message } from 'antd';
import { useGetBooksQuery, useDeleteBookMutation, useUpdateBookMutation, useCreateBookMutation } from '../redux/slices/apiSlice';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import CreateBookModal from '../components/BookModal';

const Dashboard = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [modalMode, setModalMode] = useState('create'); 
  const [currentBook, setCurrentBook] = useState(null);
  const navigate = useNavigate();

  // Fetch user's books with pagination
  const { data, isLoading, isError, error } = useGetBooksQuery({ page: currentPage, limit: pageSize });
  const [createBook] = useCreateBookMutation();
  const [deleteBook] = useDeleteBookMutation();
  const [updateBook] = useUpdateBookMutation();

  const isAuthenticated = useSelector((state) => state.auth.isAuthenticated);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  const handleDelete = async (id) => {
    try {
      await deleteBook(id).unwrap();
      message.success('Book deleted successfully!');
    } catch (err) {
      console.error('Failed to delete the book', err);
      message.error('Failed to delete book');
    }
  };

  const handleEdit = (book) => {
    setCurrentBook(book);
    setModalMode('edit');
    setIsModalVisible(true);
  };

  const showCreateModal = () => {
    setModalMode('create');
    setCurrentBook(null);
    setIsModalVisible(true);
  };

  const handleCreateOrUpdate = async (values) => {
    try {
      if (modalMode === 'create') {
        await createBook(values).unwrap();
        message.success('Book created successfully!');
      } else {
        await updateBook({ id: currentBook.id, ...values }).unwrap();
        message.success('Book updated successfully!');
      }
      setIsModalVisible(false);
    } catch (error) {
      console.error(`Failed to ${modalMode === 'create' ? 'create' : 'update'} book`, error);
      message.error(`Failed to ${modalMode === 'create' ? 'create' : 'update'} book`);
    }
  };

  const columns = [
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
    },
    {
      title: 'Author',
      dataIndex: 'author',
      key: 'author',
    },
    {
      title: 'Publication Date',
      dataIndex: 'publication_date',
      key: 'publication_date',
    },
    {
      title: 'ISBN',
      dataIndex: 'isbn',
      key: 'isbn',
    },
    {
      title: 'Cover Image',
      key: 'cover_image',
      render: (text, record) => (
        record.cover_image ? (
          <img
            src={record.cover_image}
            alt="Cover"
            style={{ width: 50, height: 50, objectFit: 'cover' }}
          />
        ) : null
      ),
    },
    {
      title: 'Action',
      key: 'action',
      render: (text, record) => (
        <Space size="middle">
          <Button type="link" onClick={() => handleEdit(record)}>Edit</Button>
          <Popconfirm
            title="Are you sure to delete this book?"
            onConfirm={() => handleDelete(record.id)}
            okText="Yes"
            cancelText="No"
          >
            <Button type="link" danger>
              Delete
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  const handlePageChange = (page, pageSize) => {
    setCurrentPage(page);
    setPageSize(pageSize);
  };

  if (isLoading) {
    return <p>Loading books...</p>;
  }

  return (
    <div>
      <h1>My Books</h1>

      <Button type="primary" onClick={showCreateModal} style={{ marginBottom: 16, float: 'right' }}>
        + Add Book
      </Button>

      {data?.books.length === 0 ? (
        <p>No books available.</p>
      ) : (
        <>
          <Table
            columns={columns}
            dataSource={data?.books || []}
            rowKey="id"
            pagination={false}
          />

          <Pagination
            current={currentPage}
            total={data?.pagination.total || 0}
            pageSize={pageSize}
            onChange={handlePageChange}
            showSizeChanger
            pageSizeOptions={[10, 20, 50]}
            showTotal={(total) => `Total ${total} items`}
          />
        </>
      )}

      <CreateBookModal
        visible={isModalVisible}
        onClose={() => setIsModalVisible(false)}
        mode={modalMode}
        bookData={currentBook}
        onCreateOrUpdate={handleCreateOrUpdate}
      />
    </div>
  );
};

export default Dashboard;
