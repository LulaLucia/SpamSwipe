use mlpteam_db;
/*already inserted
INSERT INTO user (uid, username, `name`, org_acct, email, `password`) VALUES
    (1, "CoolGoose", "Lily", 0, "li909@wellesley.edu", "G00se123!"),
    (2, "LadyBug", "Beatrice", 0, "be991@wellesley.edu", "8uggy!9Q"),
    (3, "camsdept", "Cinema & Media Studies", 1, "camsdept@wellesley.edu", "1lovem0vies!");*/

/*INSERT INTO picfile(uid, post_id, file_name) VALUES
    (1, 1, "stonegravis.png"),
    (3, 2, "movie.png"),
    (2, 3, "openhouse.png");*/

/*INSERT INTO post (post_id, uid, title, `description`, file_id, exp_date, public) VALUES
    (1, 1, "Stone Gravis", "Halloween activities at Stone Davis at 9pm on 10/30", 1, "2026-10-31", 0),
    (2, 3, "Movie Screening", "Join movie club for a screening at Collins cinema.", 2, "2026-11-02", 1),
    (3, 2, "Homestead Open House", "Learn about Homestead at Wellesley!", 3, "2026-11-12", 0);*/

INSERT INTO tag (tag_name, post_id) VALUES
    ("res life", 1),
    ("holiday", 1),
    ("crafts", 1),
    ("food", 1),
    ("movie", 2),
    ("food", 2),
    ("camsdept", 2),
    ("open house", 3),
    ("co-ops", 3);




