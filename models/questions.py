db.define_table('questions',
                Field('base_course', type='string', notnull=True),
                Field('name', type='string', notnull=True),
                Field('chapter', type='string'),  # matches chapter_label, not name
                Field('subchapter', type='string'), # matches sub_chapter_label, not name
                Field('author', type='string'),
                Field('difficulty', type='integer'),
                Field('question', type='text'),
                Field('timestamp',type='datetime'),
                Field('question_type',type='string'),
                Field('is_private', type='boolean'),
                Field('htmlsrc', type='text'),
                Field('autograde', type='string'),
                migrate='runestone_questions.table')

# In SQL we can manually add the constraint
# alter table questions add constraint name_bc_unique UNIQUE(name, base_course);
# try:
#     db.executesql('''alter table questions add constraint name_bc_unique UNIQUE(name, base_course)''')
# except:
#     pass

db.define_table('tags',
                Field('tag_name', type='string', unique=True),
                migrate='runestone_tags.table')

db.define_table('question_tags',
                Field('question_id', db.questions),
                Field('tag_id', db.tags),
                migrate='runestone_question_tags.table')

## assignment <--> questions is a many-to-many relation. This table associates them
## points and how it's autograded are properties of a particular use of a question in an assignment,
## so that different instructors (assignments) can have a different way of doing it.
db.define_table('assignment_questions',
                Field('assignment_id', db.assignments),
                Field('question_id', db.questions),
                Field('points', type='integer'),
                Field('timed', type='boolean'), #deprecated; should be a property of the assignment
                Field('autograde', type='string'), # oneof: null, all_or_nothing, pct_correct
                Field('which_to_grade', type='string'), # oneof: first_answer, last_answer, or best_answer
                Field('reading_assignment', type='boolean'), # so we can differentiate reading part of an assignment from the questions to be embedded on the assignment page
                Field('assessment_type', db.assignment_types,
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'assignment_types.id', '%(name)s'))),   # deprecated; shouldn't be property of assignment_question
                migrate='runestone_assignment_questions.table')
