CREATE TABLE LOG6307_ISSUES (
  id          integer PRIMARY KEY,
  summary     varchar,
  type        varchar(32),
  status      varchar(32),
  version     varchar(32),
  component   varchar(32),
  owner       varchar
);