CREATE TABLE todos (
        id INTEGER NOT NULL,
        title VARCHAR,
        description VARCHAR,
        priority INTEGER,
        completed BOOLEAN,
        PRIMARY KEY (id)
);
CREATE INDEX ix_todos_id ON todos (id);

INSERT INTO todos (title, description, priority, completed) VALUES ('Buy groceries', 'Milk, Bread, Eggs', 1, FALSE);
INSERT INTO todos (title, description, priority, completed) VALUES ('Clean the house', 'Living room, Kitchen, Bathroom', 2, FALSE);     

Select * from todos;

SELECT * FROM todos WHERE complete = FALSE ORDER BY priority ASC;

.mode column
.headers on

.mode markdown

.mode box

.mode table