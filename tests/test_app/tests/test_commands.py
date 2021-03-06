from datetime import timedelta
from django.core.management import CommandError
from django.utils import timezone
import reversion
from test_app.models import TestModel
from test_app.tests.base import TestBase


class CreateInitialRevisionsTest(TestBase):

    def testCreateInitialRevisions(self):
        obj = TestModel.objects.create()
        self.callCommand("createinitialrevisions")
        self.assertSingleRevision((obj,), comment="Initial version.")

    def testCreateInitialRevisionsAlreadyCreated(self):
        obj = TestModel.objects.create()
        self.callCommand("createinitialrevisions")
        self.callCommand("createinitialrevisions")
        self.assertSingleRevision((obj,), comment="Initial version.")


class CreateInitialRevisionsAppLabelTest(TestBase):

    def testCreateInitialRevisionsAppLabel(self):
        obj = TestModel.objects.create()
        self.callCommand("createinitialrevisions", "test_app")
        self.assertSingleRevision((obj,), comment="Initial version.")

    def testCreateInitialRevisionsAppLabelMissing(self):
        with self.assertRaises(CommandError):
            self.callCommand("createinitialrevisions", "boom")

    def testCreateInitialRevisionsModel(self):
        obj = TestModel.objects.create()
        self.callCommand("createinitialrevisions", "test_app.TestModel")
        self.assertSingleRevision((obj,), comment="Initial version.")

    def testCreateInitialRevisionsModelMissing(self):
        with self.assertRaises(CommandError):
            self.callCommand("createinitialrevisions", "test_app.boom")

    def testCreateInitialRevisionsModelMissingApp(self):
        with self.assertRaises(CommandError):
            self.callCommand("createinitialrevisions", "boom.boom")

    def testCreateInitialRevisionsModelNotRegistered(self):
        TestModel.objects.create()
        self.callCommand("createinitialrevisions", "auth.User")
        self.assertNoRevision()


class CreateInitialRevisionsDbTest(TestBase):

    def testCreateInitialRevisionsDb(self):
        obj = TestModel.objects.create()
        self.callCommand("createinitialrevisions", using="postgres")
        self.assertNoRevision()
        self.assertSingleRevision((obj,), comment="Initial version.", using="postgres")

    def testCreateInitialRevisionsDbMySql(self):
        obj = TestModel.objects.create()
        self.callCommand("createinitialrevisions", using="mysql")
        self.assertNoRevision()
        self.assertSingleRevision((obj,), comment="Initial version.", using="mysql")


class CreateInitialRevisionsModelDbTest(TestBase):

    def testCreateInitialRevisionsModelDb(self):
        obj = TestModel.objects.db_manager("postgres").create()
        self.callCommand("createinitialrevisions", model_db="postgres")
        self.assertSingleRevision((obj,), comment="Initial version.", model_db="postgres")


class CreateInitialRevisionsCommentTest(TestBase):

    def testCreateInitialRevisionsComment(self):
        obj = TestModel.objects.create()
        self.callCommand("createinitialrevisions", comment="comment v1")
        self.assertSingleRevision((obj,), comment="comment v1")


class DeleteRevisionsTest(TestBase):

    def testDeleteRevisions(self):
        with reversion.create_revision():
            TestModel.objects.create()
        self.callCommand("deleterevisions")
        self.assertNoRevision()


class DeleteRevisionsAppLabelTest(TestBase):

    def testDeleteRevisionsAppLabel(self):
        with reversion.create_revision():
            TestModel.objects.create()
        self.callCommand("deleterevisions", "test_app")
        self.assertNoRevision()

    def testDeleteRevisionsAppLabelMissing(self):
        with self.assertRaises(CommandError):
            self.callCommand("deleterevisions", "boom")

    def testDeleteRevisionsModel(self):
        with reversion.create_revision():
            TestModel.objects.create()
        self.callCommand("deleterevisions", "test_app.TestModel")
        self.assertNoRevision()

    def testDeleteRevisionsModelMissing(self):
        with self.assertRaises(CommandError):
            self.callCommand("deleterevisions", "test_app.boom")

    def testDeleteRevisionsModelMissingApp(self):
        with self.assertRaises(CommandError):
            self.callCommand("deleterevisions", "boom.boom")

    def testDeleteRevisionsModelNotRegistered(self):
        with reversion.create_revision():
            obj = TestModel.objects.create()
        self.callCommand("deleterevisions", "auth.User")
        self.assertSingleRevision((obj,))


class DeleteRevisionsDbTest(TestBase):

    def testDeleteRevisionsDb(self):
        with reversion.create_revision(using="postgres"):
            TestModel.objects.create()
        self.callCommand("deleterevisions", using="postgres")
        self.assertNoRevision(using="postgres")

    def testDeleteRevisionsDbMySql(self):
        with reversion.create_revision(using="mysql"):
            TestModel.objects.create()
        self.callCommand("deleterevisions", using="mysql")
        self.assertNoRevision(using="mysql")

    def testDeleteRevisionsDbNoMatch(self):
        with reversion.create_revision():
            obj = TestModel.objects.create()
        self.callCommand("deleterevisions", using="postgres")
        self.assertSingleRevision((obj,))


class DeleteRevisionsModelDbTest(TestBase):

    def testDeleteRevisionsModelDb(self):
        with reversion.create_revision():
            TestModel.objects.db_manager("postgres").create()
        self.callCommand("deleterevisions", model_db="postgres")
        self.assertNoRevision(using="postgres")


class DeleteRevisionsDaysTest(TestBase):

    def testDeleteRevisionsDays(self):
        date_created = timezone.now() - timedelta(days=20)
        with reversion.create_revision():
            TestModel.objects.create()
            reversion.set_date_created(date_created)
        self.callCommand("deleterevisions", days=19)
        self.assertNoRevision()

    def testDeleteRevisionsDaysNoMatch(self):
        date_created = timezone.now() - timedelta(days=20)
        with reversion.create_revision():
            obj = TestModel.objects.create()
            reversion.set_date_created(date_created)
        self.callCommand("deleterevisions", days=21)
        self.assertSingleRevision((obj,), date_created=date_created)


class DeleteRevisionsKeepTest(TestBase):

    def testDeleteRevisionsKeep(self):
        with reversion.create_revision():
            obj_1 = TestModel.objects.create()
            reversion.set_comment("obj_1 v1")
        with reversion.create_revision():
            obj_1.save()
            reversion.set_comment("obj_1 v2")
        with reversion.create_revision():
            obj_2 = TestModel.objects.create()
            reversion.set_comment("obj_2 v1")
        with reversion.create_revision():
            obj_2.save()
            reversion.set_comment("obj_2 v2")
        self.callCommand("deleterevisions", keep=1)
        self.assertSingleRevision((obj_1,), comment="obj_1 v2")
        self.assertSingleRevision((obj_2,), comment="obj_2 v2")
